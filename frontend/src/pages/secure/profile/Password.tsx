import React, {Dispatch, SyntheticEvent, useEffect, useState} from 'react';
import Layout from "../../../components/Layout";
import Container from "@mui/material/Container";
import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";
import Grid from "@mui/material/Grid";
import TextField from "@mui/material/TextField";
import Button from "@mui/material/Button";
import axios from "axios";

import {Redirect} from "react-router-dom";

const Password = (props: any) => {
    const [password, setPassword] = useState('');
    const [confirm_password, setConfirmPassword] = useState('');
    const [redirect, setRedirect] = useState(false);

    // useEffect(() => {
    //     setFirstName(props.user.first_name);
    //     setLastName(props.user.last_name);
    //     setEmail(props.user.email);
    //     setDateOfBirth(props.user.dob);
    //     setPhone(props.user.phone);
    //     setLocation(props.user.location);
    //     setProfileImage(props.user.profile_image);
    // }, [props.user]);


    const passwordSubmit = async (e: SyntheticEvent) => {
        e.preventDefault();
        await axios.put('users/password', {
            password,
            confirm_password
        })
    }
    if (redirect) {
        return <Redirect to='/'/>
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
                            Change Password
                        </Typography>
                        <Box component="form" noValidate onSubmit={passwordSubmit} sx={{ mt: 3 }}>
                            <Grid container spacing={2}>
                                <Grid item xs={12}>
                                    <TextField
                                        required
                                        fullWidth
                                        name="password"
                                        label="Password"
                                        type="password"
                                        id="password"
                                        autoComplete="new-password"
                                        onChange={e => setPassword(e.target.value)}
                                    />
                                </Grid>
                                <Grid item xs={12}>
                                    <TextField
                                        required
                                        fullWidth
                                        name="password"
                                        label="Confirm Password"
                                        type="password"
                                        id="confirm_password"
                                        autoComplete="new-password"
                                        onChange={e => setConfirmPassword(e.target.value)}
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

export default (Password);