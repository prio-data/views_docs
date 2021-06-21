
from unittest import TestCase
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from inspector import crud, models

class TestCrud(TestCase):
    def setUp(self):
        engine = create_engine("sqlite:///:memory:")
        models.Base.metadata.create_all(engine)
        self.session = sessionmaker(engine)()

    def test_get_or_create_one(self):
        crud.get_or_create_path(self.session, "foo","bar")
        self.session.commit()

        self.assertEqual(self.session.query(models.Host).count(),1)
        self.assertEqual(self.session.query(models.Path).count(),1)

    def test_get_or_create_two(self):
        crud.get_or_create_path(self.session, "foo","bar")
        self.session.commit()

        crud.get_or_create_path(self.session, "foo","baz")
        self.session.commit()

        self.assertEqual(self.session.query(models.Host).count(),1)
        self.assertEqual(self.session.query(models.Path).count(),2)

        self.assertEqual(self.session.query(models.Host).first().name,"foo")
        self.assertEqual(
                {p.name for p in self.session.query(models.Path).all()},
                {"bar","baz"}
                )

    def test_cascade(self):
        crud.get_or_create_path(self.session, "foo", "bar")
        crud.get_or_create_path(self.session, "foo", "baz")
        self.session.commit()

        crud.delete_host(self.session, "foo")
        self.session.commit()

        for model in (models.Host, models.Path):
            self.assertEqual(self.session.query(model).count(), 0)

    def test_annotate(self):
        crud.get_or_create_path(self.session, "foo", "bar")
        crud.annotate_path(self.session, "foo", "bar", "yeehaw")
        self.assertEqual(crud.get_annotation(self.session, "foo","bar"), "yeehaw")
        self.assertEqual(crud.get_annotation(self.session, "foo","baz"), "")

    def test_list_annotation(self):
        crud.annotate_path(self.session, "alpha", "beta", "alpha")
        crud.annotate_path(self.session, "alpha", "gamma", "beta")
        crud.annotate_path(self.session, "alpha", "epsilon", "gamma")

        crud.annotate_path(self.session, "nothing", "nowhere", "gamma")

        annotations = crud.list_annotations(self.session, "alpha")
        self.assertEqual({*annotations.values()},{"alpha","beta","gamma"})
        self.assertEqual({*annotations.keys()},{"beta","gamma","epsilon"})
