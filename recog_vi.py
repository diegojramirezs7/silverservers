from voiceit2 import VoiceIt2

# users can be given their token to authenticate, so that they don't have use developers' keys and tokens
# if using token authentication: voiceit = VoiceIt2("user_token", "")
# only allows to API calls related to that user
voiceit = VoiceIt2("key_d79251d085214874b7479cdf67cd40b8", "tok_3f628df367944320a359510086825836")

#alternative url that receives results of API calls
voiceit.add_notification_url("some url")

# all approved phrases for verification
my_voiceit.get_phrases("en-CA") # could be en-US

voiceit.get_all_users()

voiceit.create_user()

voiceit.check_user_exists("userId")

voiceit.get_groups_for_user("userId")

voiceit.create_user_token("<userId>", "secs to timeout")

voiceit.expire_user_tokens("userId")

# group methods: get_all(), check_exists("groupId"), get_group("gid"), create_group("description")
# add_user_to_group(gid, uid), remove_user_from_group(gid, uid), delete_group("gid")


