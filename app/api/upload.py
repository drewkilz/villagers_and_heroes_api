from datetime import datetime, timezone
from http import HTTPStatus
import os
import os.path
import time
from itertools import count
from threading import Thread

from flask import request, current_app, jsonify, make_response, url_for
from werkzeug.utils import secure_filename

from app import create_app
from app.api import api
from app.village import VillageImageParser
from app.village.roster.snapshot import SnapshotSchema
from configuration import ENV_VNH_UPLOAD_FOLDER, ENV_FLASK_CONFIGURATION, DEVELOPMENT_KEY

_jobs = {}
_job_counter = count().__next__


class UploadJob(Thread):
    def __init__(self, original_images, image_paths, dates, server):
        super(UploadJob, self).__init__()

        self.original_images = original_images
        self.image_paths = image_paths
        self.dates = dates
        self.id = _job_counter()
        self.return_value = None
        self.server = server

    def run(self):
        app = create_app(os.getenv(ENV_FLASK_CONFIGURATION) or DEVELOPMENT_KEY)
        app.app_context().push()

        parser = VillageImageParser(self.server)

        try:
            for original_image, image_path, date in zip(self.original_images, self.image_paths, self.dates):
                timestamp = datetime.fromtimestamp(int(date) / 1000.0, tz=timezone.utc)
                modified_time = time.mktime(timestamp.astimezone().timetuple())
                os.utime(image_path, (modified_time, modified_time))

                parser.add_image(original_image, image_path)

            parser.process()

            parser.save()
        finally:
            # Clean up temporary uploaded files
            for path in self.image_paths:
                if os.path.exists(path):
                    os.remove(path)

        data = {
            'processing_time': parser.processing_time,
            'village': parser.village,
            'server': parser.server,
            'roster': [],
            'projects': []
        }

        if parser.roster and parser.roster.snapshots:
            data['roster'] = SnapshotSchema(many=True).dump(parser.roster.snapshots)

        self.return_value = jsonify(data)


@api.route('/village/upload/', methods=['POST'])
def upload_images():
    if 'images' not in request.files:
        return jsonify({'error': 'No "images" in provided files.'}), HTTPStatus.BAD_REQUEST

    if 'imageDates' not in request.form:
        return jsonify({'error': 'No "imageDates" in provided form.'}), HTTPStatus.BAD_REQUEST

    if 'server' not in request.form:
        return jsonify({'error': 'No "server" in provided form.'}), HTTPStatus.BAD_REQUEST

    # Grab the data
    images = request.files.getlist('images')
    dates = request.form.getlist('imageDates')
    server = request.form['server']

    # Save the files locally
    saved_image_paths = []
    original_image_paths = []
    for image in images:
        original_image_paths.append(image.filename)
        new_filename = secure_filename(image.filename)
        new_filepath = os.path.join(current_app.config[ENV_VNH_UPLOAD_FOLDER], new_filename)
        saved_image_paths.append(new_filepath)
        image.save(new_filepath)

    # Create a job and add to the queue
    job = UploadJob(original_image_paths, saved_image_paths, dates, server)
    _jobs[job.id] = job
    job.start()

    # Generate some return data defining information about the job
    data = {
        'id': job.id,
        'submitted_at': datetime.now(),
        'status_url': url_for('api.upload_status', _external=True, id_=job.id)
    }

    # Create the response with the return data and a location of the status url
    response = make_response(jsonify(data), HTTPStatus.ACCEPTED)
    response.headers['Location'] = data['status_url']
    response.headers['Retry-After'] = 5
    response.headers['Access-Control-Expose-Headers'] = 'Location, Retry-After'

    return response


@api.route('/village/upload/status/<int:id_>')
def upload_status(id_):
    if id_ not in _jobs:
        return jsonify({'error': 'No job with id: "{}" found.'.format(id_)}), HTTPStatus.BAD_REQUEST

    job = _jobs[id_]

    if job.return_value:
        # Remove from the queue
        _jobs.pop(id_)

        # Return the result
        return job.return_value

    # No return value yet, so send a status location
    response = make_response('', HTTPStatus.ACCEPTED)
    response.headers['Location'] = url_for('api.upload_status', _external=True, id_=id_)
    response.headers['Retry-After'] = 5
    response.headers['Access-Control-Expose-Headers'] = 'Location, Retry-After'

    return response
