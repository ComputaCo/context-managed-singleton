import unittest
from context_managed_singleton import ContextManagedSingleton


class TestContextManagedSingleton(unittest.TestCase):
    def test_without_baked_object(self):
        ctx = ContextManagedSingleton()
        self.assertIsInstance(ctx, ContextManagedSingleton)

    def test_init_with_dict(self):
        ctx = ContextManagedSingleton({"a": 1, "b": 2})
        self.assertEqual(ctx.a, 1)
        self.assertEqual(ctx.b, 2)

    def test_init_with_object(self):
        class Dummy:
            a = 1
            b = 2

        ctx = ContextManagedSingleton(Dummy())
        self.assertEqual(ctx.a, 1)
        self.assertEqual(ctx.b, 2)

    def test_nested_context_managed_singleton(self):
        with ContextManagedSingleton({"name": "Jacob"}) as outer_ctx:
            self.assertEqual(outer_ctx.name, "Jacob")
            with ContextManagedSingleton({"name": "Isaac"}) as inner_ctx:
                self.assertEqual(inner_ctx.name, "Isaac")
                self.assertEqual(outer_ctx.name, "Jacob")
            self.assertEqual(outer_ctx.name, "Jacob")

    def test_jagged_nested_context_managed_singleton(self):
        with ContextManagedSingleton(
            {"name": "Jacob", "a": 1}, getattr_recursive=True
        ) as outer_ctx:
            with ContextManagedSingleton(
                {"name": "Isaac"}, getattr_recursive=True
            ) as inner_ctx:
                self.assertEqual(inner_ctx.a, 1)

    def test_asymmetric_exit_error(self):
        ctx1 = ContextManagedSingleton({"name": "Jacob"})
        ctx2 = ContextManagedSingleton({"name": "Isaac"})
        ctx1.__enter__()
        ctx2.__enter__()
        with self.assertRaises(AssertionError):
            ctx1.__exit__(None, None, None)

    def test_no_current_context_managed_singleton_raises_error(self):
        class Foo(ContextManagedSingleton):
            pass

        with self.assertRaises(RuntimeError):
            current = Foo.current()
            print("current inside", current.__dict__)

    def test_subclassed_context_managed_singleton1(self):
        class Dummy(ContextManagedSingleton):
            pass

        ctx = Dummy({"name": "Jacob"})
        self.assertEqual(ctx.name, "Jacob")

    def test_subclassed_context_managed_singleton2(self):
        class Dummy(ContextManagedSingleton):
            a: str = None
            b: str = None

        with Dummy() as ctx:
            ctx.a = "foo"
            Dummy.current().b = "bar"
            self.assertEqual(Dummy.current().a, "foo")
            self.assertEqual(ctx.b, "bar")

    def test_wrapped_context_managed_singleton(self):
        class Dummy:
            a: str = None
            b: str = None

        WrappedDummy = ContextManagedSingleton.wrap(Dummy)
        with WrappedDummy() as ctx:
            ctx.a = "foo"
            WrappedDummy.current().b = "bar"
            self.assertEqual(WrappedDummy.current().a, "foo")
            self.assertEqual(ctx.b, "bar")


if __name__ == "__main__":
    unittest.main()
