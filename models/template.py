from mongoengine import Document, StringField, SequenceField


class Template(Document):
    """
    ODM for Template documents.
    """

    template_id = SequenceField(unique=True)
    template_name = StringField(max_length=50, required=True)
    subject = StringField(max_length=100, required=True)
    body = StringField(max_length=255, required=True)
    author_id = StringField(min_length=24, max_length=50)
