def handle(req, logger):
    """handle a request to the function
    Args:
        req (str): request body
        logger: print log into stderr
    """
    logger.info("started")
    logger.info("invoke function1")
    return req
