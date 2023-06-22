import React, {Dispatch, useEffect, useState} from 'react';
import axios from "axios";
import {connect} from "react-redux";
import {createTheme, ThemeProvider} from "@mui/material/styles";
import Container from "@mui/material/Container";
import {Divider} from "@mui/material";
import {Redirect} from "react-router-dom";

import {setUser} from "../redux/actions/setUserAction";
import {User} from '../models/user'
import Footer from "./Footer";
import Header from "./Header";

const defaultTheme = createTheme();
const Layout = (props: any) => {
    const [redirect, setRedirect] = useState(false);

    useEffect(() => {
        (
            async () => {
                try {
                    const {data} = await axios.get('user');

                    props.setUser(data.data);
                } catch (e) {
                    setRedirect(true);
                }
            }
        )();
    }, []);

    if (redirect) {
        return <Redirect to='/login'/>
    }

    return (
        <>
            <Header />
            <ThemeProvider theme={defaultTheme}>
                <Container maxWidth="lg">
                    <main>
                        <Divider />
                        {props.children}
                    </main>
                </Container>
            </ThemeProvider>
            <Footer />
        </>
    );
};

const mapStateToProps = (state: { user: User }) => ({
    user: state.user
})

const mapDispatchToProps = (dispatch: Dispatch<any>) => ({
    setUser: (user: User) => dispatch(setUser(user))
})

export default connect(mapStateToProps, mapDispatchToProps)(Layout);