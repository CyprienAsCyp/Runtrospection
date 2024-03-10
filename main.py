from runtrospection.authentication import Authenticator
from runtrospection.strava_app import StravaApp


def main():
    auth = Authenticator()
    print(auth.access_token)


if __name__ == "__main__":
    main()
