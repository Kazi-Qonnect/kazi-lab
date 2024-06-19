from models import User,db,Role,Service, County
from app import app

with app.app_context():
    new_user = Service(
        service_name='salman',
        provider_id=1,
    )
    # db.session.add(new_user)
    # db.session.commit()

    roles = []
    for role_name in ['admin','provider','client']:
        role = Role(role_name=role_name)
        roles.append(role)

        # db.session.add_all(roles)
        # db.session.commit()

    counties = []
    for county_name in ['']:
        county = County(county_name=county_name)
        counties.append(county)

        db.session.add_all(counties)
        db.session.commit()
        
