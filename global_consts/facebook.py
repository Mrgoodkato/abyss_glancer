FB_HEADER_INFO = {
    "header": "x-fb-friendly-name",
    "header_val": "CometSinglePostDialogContentQuery"
}
FB_URL_API = "api/graphql/"
FB_HEADER_KEY = "x-fb-friendly-name"
FB_HEADER_VALUES = {
    "main_comment_load": "CometSinglePostDialogContentQuery",
    "comments_section": "CommentsListComponentsPaginationQuery"
}
FB_COMMENT_SHAPE = {
    "layer1": "data",
    "layer2": "node_v2",
    "layer3": "comet_sections",
    "layer4": "feedback",
    "layer5": "story",
    "layer6": "story_ufi_container",
    "layer7": "story",
    "layer8": "feedback_context",
    "layer8_1": "feedback_target_with_context", # Too lazy to number these again
    "layer9": "comment_list_renderer",
    "layer10": "feedback",
    "layer11": "comment_rendering_instance_for_feed_location",
    "layer12": "comments",
    "layer13": "edges"
}
FB_PAGINATION_COMMENT_SHAPE = {
    "layer1": "node",
    "layer2": "comment_rendering_instance_for_feed_location",
    "layer3": "comments",
    "layer4": "edges"
}
FB_COMMENT_MODE_MAP = {
    "main_comment_load": FB_COMMENT_SHAPE,
    "comments_section": FB_PAGINATION_COMMENT_SHAPE
}