class Post_Reaction():

    """class to create a post reaction instance
    """
    def __init__(self, id, user_id, reaction_id, post_id):
        self.id = id
        self.user_id = user_id
        self.reaction_id = reaction_id
        self.post_id = post_id
