from flask import request,jsonify,Blueprint, redirect,url_for, flash
def construct_blueprint(cluster):
    data = Blueprint("data",__name__,url_prefix="/api")

    @data.route("/team",methods=["GET"])    #RETURNS ALL TEAM MEMBERS
    def get_team_all():
        response = cluster.db.team_members.find()
        output = []
        if response:
            for member in response:
                member_data = {
                    "name" : member["name"],
                    "dept" : member["dept"],
                    "rollno" : member["rollno"],
                    "email" : member["email"],
                    "about" : member["about"],
                    "github" : member["github"],
                    "linkedin" : member["linkedin"],
                    "avatar" : member["avatar"]
                }
                output.append(member_data)
            return jsonify({"status" : 200,"result": output})
        return jsonify({"status" : 404,"result": "no data"})

    @data.route("/team",methods=["POST"])     #ADDS TEAM MEMBER
    def add_team_member():
        name = request.form.get("name")
        dept = request.form.get("dept")
        rollno = request.form.get("rollno")
        email = request.form.get("email")
        about = request.form.get("about")
        github = request.form.get("github")
        linkedin = request.form.get("linkedin")
        avatar = request.form.get("avatar")
        response = cluster.db.team_members.find_one({"rollno" : rollno})
        if response:
            response = cluster.db.team_members.update_one(
                        {"rollno" : rollno} ,
                        { "$set" : 
                            {
                                "name" : name,
                                "dept" : dept,
                                "rollno" : rollno,
                                "email" : email,
                                "about" : about,
                                "github" : github,
                                "linkedin" : linkedin,
                                "avatar" : avatar
                            }
                        }
            )
            if response:
                flash('Member updated successfully','success')
                return redirect(url_for('admin.add_members'))
            flash('Member cannot be updated','error')
            return redirect(url_for('admin.add_members'))
        else:
            response = cluster.db.team_members.insert_one(
                    {
                        "name" : name,
                        "dept" : dept,
                        "rollno" : rollno,
                        "email" : email,
                        "about" : about,
                        "github" : github,
                        "linkedin" : linkedin,
                        "avatar" : avatar
                    }
            )
            if response:
                flash('Member added successfully','success')
                return redirect(url_for('admin.add_members'))
            flash('Member cannot be added','error')
            return redirect(url_for('admin.add_members'))

    return data