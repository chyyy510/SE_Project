class GeneratePath:
    @classmethod
    def generate_path_avatar(cls, instance, filename):
        return "avatar/user_{0}/{1}".format(instance.user.uid, filename)
