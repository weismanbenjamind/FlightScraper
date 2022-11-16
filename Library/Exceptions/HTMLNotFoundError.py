class HTMLNotFoundError(Exception):

    def __init__(self, element_description: str):
        super().__init__(f'Could not find HTML for {element_description}')