from flask import request, redirect, jsonify
import uuid

def authorize():
    """
    Handle the authorization request.

    This function generates an authorization code and redirects the user to the provided redirect URI
    with the authorization code and state as query parameters.

    Returns:
        Response: A redirect response to the redirect URI with the authorization code and state.
    """
    from .oauth2_server import AuthorizationCode, authorization_codes

    client_id = request.args.get('client_id')
    redirect_uri = request.args.get('redirect_uri')
    scope = request.args.get('scope')
    state = request.args.get('state')
    response_type = request.args.get('response_type')

    code = str(uuid.uuid4())
    authorization_codes[code] = AuthorizationCode(
        code=code,
        client_id=client_id,
        redirect_uri=redirect_uri,
        scope=scope,
        state=state,
    )

    return redirect(f"{redirect_uri}?code={code}&state={state}")

def token():
    """
    Handle the token request.

    This function validates the authorization code and client information, then generates an access token
    if the validation is successful.

    Returns:
        Response: A JSON response containing the access token and related information, or an error message.
    """
    from .oauth2_server import authorization_codes, logger

    code = request.form.get('code')
    client_id = request.form.get('client_id')
    redirect_uri = request.form.get('redirect_uri')

    logger.info(f"Token request received: code={code}, client_id={client_id}, redirect_uri={redirect_uri}")

    if code not in authorization_codes:
        logger.error("Invalid or expired authorization code.")
        return jsonify({"error": "invalid_grant"}), 400

    auth_code_data = authorization_codes.pop(code)

    if auth_code_data.client_id != client_id or auth_code_data.redirect_uri != redirect_uri:
        logger.error("Invalid client_id or redirect_uri.")
        return jsonify({"error": "invalid_client"}), 400

    access_token = str(uuid.uuid4())
    logger.info(f"Access token generated: {access_token}")

    return jsonify({
        "access_token": access_token,
        "token_type": "Bearer",
        "expires_in": 3600,
        "scope": auth_code_data.scope,
    })