import React, {SyntheticEvent, useEffect, useState} from 'react';
import Avatar from '@mui/material/Avatar';
import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';
import Link from '@mui/material/Link';
import Grid from '@mui/material/Grid';
import Box from '@mui/material/Box';
import LockOutlinedIcon from '@mui/icons-material/LockOutlined';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import MenuItem from '@mui/material/MenuItem';
import Select, { SelectChangeEvent } from '@mui/material/Select';
import axios from "axios";
import {Redirect} from "react-router-dom";
import {FormHelperText} from "@mui/material";

import {Role} from "../models/role";



function Copyright(props: any) {
    return (
        <Typography variant="body2" color="text.secondary" align="center" {...props}>
            {'Copyright © '}
            <Link color="inherit">
                Isotopes Music
            </Link>{' '}
            {new Date().getFullYear()}
            {'.'}
        </Typography>
    );
}

const defaultTheme = createTheme();

const Register = () => {
    const [first_name, setFirstName] =useState('')
    const [last_name, setLastName] = useState('')
    const [email, setEmail] = useState('');
    const [role_id, setRoleID] = useState(0);
    const [roles, setRoles] = useState<Role[]>([])
    const [password, setPassword] = useState('');
    const [confirm_password, setConfirmPassword] = useState('');
    const [redirect, setRedirect] = useState(false);

    useEffect(() => {
        (
            async () => {
                const response = await axios.get('roles');

                setRoles(response.data.data);
            }
        )()
    }, []);
    const submit = async (e: SyntheticEvent) => {
        e.preventDefault();

        await axios.post('register', {
            first_name,
            last_name,
            role_id,
            email,
            password,
            confirm_password
        });
        // setIsLoading(true);
        setRedirect(true);
        // setIsLoading(false)
    }
    const handleChange = (event: SelectChangeEvent) => {
        setRoleID(parseInt(event.target.value));
    };

    if (redirect) {
        return <Redirect to={'/login'}/>;
    }

    return (
        <ThemeProvider theme={defaultTheme}>
            <Container component="main" maxWidth="xs">
                <Box
                    sx={{
                        marginTop: 8,
                        display: 'flex',
                        flexDirection: 'column',
                        alignItems: 'center',
                    }}
                >
                    <Avatar sx={{ m: 1, bgcolor: 'secondary.main' }}>
                        <LockOutlinedIcon />
                    </Avatar>
                    <Typography component="h1" variant="h5">
                        Sign up
                    </Typography>
                    <Box component="form" noValidate onSubmit={submit} sx={{ mt: 3 }}>
                        <Grid container spacing={2}>
                            <Grid item xs={12} sm={6}>
                                <TextField
                                    autoComplete="given-name"
                                    name="firstName"
                                    required
                                    fullWidth
                                    id="firstName"
                                    label="First Name"
                                    autoFocus
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
                                    autoComplete="family-name"
                                    onChange={e => setLastName(e.target.value)}
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
                                    onChange={e => setEmail(e.target.value)}
                                />
                            </Grid>
                            <Grid item xs={12} >
                            <Select
                                fullWidth
                                onChange={handleChange}
                            >
                                <MenuItem disabled value="">
                                    <em>Isotope type</em>
                                </MenuItem>
                                {roles.map((role:Role) => (
                                    <MenuItem
                                        key={role.id}
                                        value={role.id}
                                    >
                                        {role.name}
                                    </MenuItem>
                                ))}
                            </Select>
                                <FormHelperText>Select Isotope Type</FormHelperText>
                            </Grid>
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
                            Sign Up
                        </Button>
                        <Grid container justifyContent="flex-end">
                            <Grid item>
                                <Link href={'/login'} variant="body2">
                                    Already have an account? Sign in
                                </Link>
                            </Grid>
                        </Grid>
                    </Box>
                </Box>
                <Copyright sx={{ mt: 5 }} />
            </Container>
        </ThemeProvider>
    );
};

export default Register;