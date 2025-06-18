class UserActivityQueryBuilder:
    def __init__(self):
        self.list_fields = ["""
                ... on ListActivity {
                    id
                    type"""]
        self.text_fields = []
        self.message_fields = ["""
        ... on MessageActivity {
            id
            type"""]
        self.fields = []

    def _add_field(self, field: str, activity_type: str):
        if activity_type.lower() == "list":
            self.list_fields.append(field)
        elif activity_type.lower() == "text":
            self.text_fields.append(field)
        elif activity_type.lower() == "message":
            self.message_fields.append(field)
        return self

    def include_list_activity_replies(self):
        return self._add_field("""
                    replyCount
                    isLocked
                    isSubscribed
                    isLiked
                    isPinned
                    likeCount""", "list")

    def include_list_activity_progress(self):
        return self._add_field("""
                    status
                    progress""", "list")

    def include_list_activity_created_at(self):
        return self._add_field("""
                    createdAt""", "list")

    def include_list_activity_user(self):
        return self._add_field("""
                    user {
                        id
                        name
                        avatar {
                            large
                        }
                    }""", "list")

    def include_list_activity_media(self):
        return self._add_field("""
                    media {
                        id
                        type
                        status(version:2)
                        isAdult
                        bannerImage
                        title {
                            userPreferred
                        }
                        coverImage {
                            large
                        }
                    }""", "list")


    def include_text_activity(self):
        return self._add_field("""
                ... on TextActivity {
                    id
                    type
                    text
                    replyCount
                    isLocked
                    isSubscribed
                    isLiked
                    isPinned
                    likeCount
                    createdAt
                    user {
                        id
                        name
                        avatar {
                            large
                        }
                    }
                }""", "text")



    def include_message_activity_content(self):
        return self._add_field("""
                    message
                    replyCount
                    isPrivate
                    isLocked
                    isSubscribed
                    isLiked
                    likeCount""", "message")

    def include_message_activity_created_at(self):
        return self._add_field("""
                    createdAt""", "message")

    def include_message_activity_recipient(self):
        return self._add_field("""
                    user: recipient {
                        id
                    }""", "message")

    def include_message_activity_messenger(self):
        return self._add_field("""
                    messenger {
                        id
                        name
                        donatorTier
                        donatorBadge
                        moderatorRoles
                        avatar {
                            large
                        }
                    }""", "message")

    def build(self):
        activity_fields = ""
        if len(self.message_fields)>1:
            message_field_str = ", ".join(self.message_fields) + "}"
            activity_fields += message_field_str
        if len(self.list_fields)>1:
            list_field_str = ", ".join(self.list_fields) + "}"
            activity_fields += list_field_str
        if len(self.text_fields)>=1:
            text_field_str = ", ".join(self.text_fields)
            activity_fields += text_field_str
        return f"""
        query($id:Int, $type:ActivityType, $page:Int, $perPage: Int) {{
            Page(page:$page, perPage:$perPage) {{
                pageInfo {{
                    total
                    perPage
                    currentPage
                    lastPage
                    hasNextPage
                }}
                activities(userId:$id, type:$type, sort:[PINNED, ID_DESC]) {{
                    {activity_fields}
                }}
            }}
        }}
        """.strip()


if __name__ == '__main__':
    query = UserActivityQueryBuilder().include_list_activity_user().build()
    print(query)