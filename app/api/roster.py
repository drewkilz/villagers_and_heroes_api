from http import HTTPStatus

from app.api import api
from app.village.roster import Roster


@api.route('/roster/')
def test_roster():
    Roster().test()

    # Returning no content as 404s are considered errors and cause logging on the UI side
    return '', HTTPStatus.NO_CONTENT
