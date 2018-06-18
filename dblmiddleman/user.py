class User:
    def __init__(self, *, data):
        self.id = data["id"]
        self.username = data["username"]
        self.discriminator = data["discriminator"]
        self.avatar = data.get("avatar")
        self.defAvatar = data["defAvatar"]
        self.bio = data.get("bio")
        self.banner = data.get("banner")
        self.social = data.get("social", {})
        self.color = data.get("color")
        self.supporter = data["supporter"]
        self.certified_dev = data["certifiedDev"]
        self.mod = data["mod"]
        self.webMod = data["webMod"]
        self.admin = data["admin"]
    
    @property
    def default_avatar(self):
        return "https://discordapp.com/assets/{0.defAvatar}.png".format(self)
    
    @property
    def avatar_url(self):
        if not self.avatar:
            return self.default_avatar
        return "https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.png".format(self)
    
    @property
    def mention(self):
        return "<@{0.id}>".format(self)