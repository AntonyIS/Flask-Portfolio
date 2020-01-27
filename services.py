def comment_count(project_id):
    comments = Comment.query.filter_by(project_id=project_id)
    return len(comments)