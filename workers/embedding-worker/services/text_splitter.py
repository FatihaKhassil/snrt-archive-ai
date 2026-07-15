from langchain_text_splitters import (
    RecursiveCharacterTextSplitter
)


class TextSplitter:

    def __init__(self):

        self.splitter = RecursiveCharacterTextSplitter(

            chunk_size=1000,

            chunk_overlap=200,

            separators=[
                "\n\n",
                "\n",
                ". ",
                " ",
                ""
            ]

        )


    def split(
        self,
        text
    ):

        return self.splitter.split_text(
            text
        )