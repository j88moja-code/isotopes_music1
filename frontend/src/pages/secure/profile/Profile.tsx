import React, {Dispatch, SyntheticEvent, useEffect, useState} from 'react';
import Layout from "../../../components/Layout";
import Container from "@mui/material/Container";
import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";
import Grid from "@mui/material/Grid";
import TextField from "@mui/material/TextField";
import Link from '@mui/material/Link';
import {Divider} from "@mui/material";
import Button from "@mui/material/Button";
import axios from "axios";
import {connect} from "react-redux";

import {User} from '../../../models/user';
import {setUser} from "../../../redux/actions/setUserAction";

const Profile = (props: any) => {
    const [first_name, setFirstName] =useState('')
    const [last_name, setLastName] = useState('')
    const [email, setEmail] = useState('');
    const [dob, setDateOfBirth] = useState('');
    const [phone, setPhone] = useState('');
    const [location, setLocation] = useState('');
    const [profile_image, setProfileImage] = useState('');
    const [redirect, setRedirect] = useState(false);

    useEffect(() => {
        setFirstName(props.user.first_name);
        setLastName(props.user.last_name);
        setEmail(props.user.email);
        setDateOfBirth(props.user.dob);
        setPhone(props.user.phone);
        setLocation(props.user.location);
        setProfileImage(props.user.profile_image);
    }, [props.user]);

    const infoSubmit = async (e: SyntheticEvent) => {
        e.preventDefault();

        await axios.put('users/info', {
            first_name,
            last_name,
            email,
            dob,
            phone,
            location
        })
    }

    return (
        <Layout>
            <Container component="main" maxWidth="xs">
                <Box
                    sx={{
                        marginTop: 8,
                        display: 'flex',
                        flexDirection: 'column',
                        alignItems: 'center',
                    }}
                    >
                    <Typography component="h1" variant="h5">
                        User Profile
                    </Typography>
                    <Typography component="h3" variant="h5">
                        Account Information
                    </Typography>
                        <Box component="form" noValidate onSubmit={infoSubmit} sx={{ mt: 3 }}>
                            <Grid container spacing={2}>
                                <Grid item xs={12} sm={6}>
                                    <TextField
                                        autoComplete="given-name"
                                        name="firstName"
                                        required
                                        fullWidth
                                        id="firstName"
                                        label="First Name"
                                        value={first_name}
                                        onChange={e => setFirstName(e.target.value)}
                                    />
                                </Grid>
                                <Grid item xs={12} sm={6}>
                                    <TextField
                                        required
                                        fullWidth
                                        id="lastName"
                                        label="Last Name"
                                        name="lastName"
                                        value={last_name}
                                        onChange={e => setLastName(e.target.value)}
                                    />
                                </Grid>
                                <Grid item xs={12} sm={6}>
                                    <TextField
                                        fullWidth
                                        id="phone"
                                        label="Phone"
                                        name="phone"
                                        value={phone}
                                        onChange={e => setPhone(e.target.value)}
                                    />
                                </Grid>
                                <Grid item xs={12} sm={6}>
                                    <TextField
                                        fullWidth
                                        id="location"
                                        label="Location"
                                        name="location"
                                        value={location}
                                        onChange={e => setLocation(e.target.value)}
                                    />
                                </Grid>
                                <Grid item xs={12}>
                                    <TextField
                                        fullWidth
                                        id="dateOfBirth"
                                        label="Date of Birth"
                                        name="dob"
                                        type="date"
                                        value={dob}
                                        onChange={e => setDateOfBirth(e.target.value)}
                                    />
                                </Grid>
                                <Grid item xs={12}>
                                    <TextField
                                        required
                                        fullWidth
                                        id="email"
                                        label="Email Address"
                                        name="email"
                                        autoComplete="email"
                                        value={email}
                                        onChange={e => setEmail(e.target.value)}
                                    />
                                </Grid>
                            </Grid>
                                <Button
                                    type="submit"
                                    fullWidth
                                    variant="contained"
                                    sx={{ mt: 3, mb: 2 }}
                                >
                                    Submit
                                </Button>
                        </Box>
                    </Box>
            </Container>
        </Layout>
    );
};

export default connect(
    (state: { user: User }) => ({
        user: state.user
    }),
    (dispatch: Dispatch<any>) => ({
        setUser: (user: User) => dispatch(setUser(user))
    })
)(Profile);