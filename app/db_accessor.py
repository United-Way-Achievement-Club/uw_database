from app import db, models

def loginUser(username, password):
    match = models.User.query.get(username)
    print models.User.query.all()
    print username
    print match
    if match == None:
        return None
    if password != match.password:
        return None
    return match

def getMembers():
    return models.Member.query.all()

def getCoordinators():
    return models.Coordinator.query.all()

def addMember(member_obj):
    general = member_obj['general']
    enrollment_form = member_obj['enrollment_form']
    demographic_data = member_obj['demographic_data']
    self_sufficiency_matrix = member_obj['self_sufficiency_matrix']
    self_efficacy_quiz = member_obj['self_efficacy_quiz']
    # TODO: parse values from these objects and create a new member based on them
    # db.session.add(models.User(username=username ...))
    # db.session.add(models.Member(username=username ...))
    # db.session.commit()