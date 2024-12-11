

BASE_ROUTE = "genemail"


def register_email_api(app, root="api"):
    from .controller import router as genemail_router

    app.include_router(genemail_router, prefix=f"/{root}/{BASE_ROUTE}")
