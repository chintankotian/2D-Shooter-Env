class test(object):
    def __init__(self):
        self.taste = 0

    def test(self):
        print(self.taste)
        return self.taste

    def get_inner_object(self):
        return self.inner(self)

    class inner(object):
        def __init__(self,outer):
            print(outer.taste)
            outer.taste += 1
            print('inside inner')
            # no = outer.test(self)
            # no += 1
            # print(no)


x = test()


x.get_inner_object()

print(x.taste)