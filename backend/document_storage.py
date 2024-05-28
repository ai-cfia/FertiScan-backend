class DocumentStorage:
    def __init__(self):
        self.document = []

    def add_page(self, page):
        if isinstance(page, str):
            if not os.path.exists(page):
                raise FileNotFoundError(f"The file {page} does not exist.")
            file = open(page)
            image = file.read()
            file.close()
        elif isinstance(page, bytes):
            image = page
        else:
            raise ValueError("The document must be a file path (str) or in bytes format.")

        self.document.append(image)

    def get_document(self) -> bytes:
        # Ensure there are images to merge
        if not self.document:
            raise ValueError("No images to merge.")

        # We only support one file at a time. 
        return self.document[0]
