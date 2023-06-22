import {Permission} from "./permission";

export interface Role {
    id: number;
    name: string;
    permissions: Permission[];

    // constructor(id = 0, name = '', permissions = []) {
    //     this.id = id;
    //     this.name = name;
    //     this.permissions = permissions;
    // }
}