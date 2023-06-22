import {Role} from "./role";

export class User {
    id!: string;
    first_name!: string;
    last_name!: string;
    email!: string;
    gender!: string;
    dob!: string;
    phone!: string;
    bio!: string;
    location!: string;
    profile_image!: string;
    role!: Role[];
    permissions!: string[];

    // constructor(id = '', first_name = '', last_name = '', email = '', gender = '', dob = '', phone = '', bio = '', location = '', profile_image = '', role = new Role(), permissions: string[] = []) {
    //     this.id = id;
    //     this.first_name = first_name;
    //     this.last_name = last_name;
    //     this.email = email;
    //     this.gender = gender;
    //     this.dob = dob;
    //     this.phone = phone;
    //     this.bio = bio;
    //     this.location = location;
    //     this.profile_image = profile_image;
    //     this.role = role;
    //     this.permissions = permissions;
    // }
}