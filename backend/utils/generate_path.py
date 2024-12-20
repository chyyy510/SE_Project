class GeneratePath:
    @classmethod
    def generate_path_avatar(cls, instance, filename):
        return "avatar/user_{0}/{1}".format(instance.user.uid, filename)

    def generate_path_experiment(cls, instance, filename):
        return "experiement/eid_{0}/{1}".format(instance.id, filename)
