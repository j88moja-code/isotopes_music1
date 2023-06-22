import React, {useEffect, useState} from 'react';
import Box from '@mui/material/Box';
import Paper from '@mui/material/Paper';
import Grid from '@mui/material/Grid';
import Layout from "../../components/Layout";
import Typography from "@mui/material/Typography";
import axios from "axios";

const Home = () => {
    const [users, setUsers] = useState([]);

    useEffect(() => {
        (
            async () => {
                const {data} = await axios.get('users');

                setUsers(data.data);
            }

        )()
    })

    return (
        <Layout>
            <Box sx={{ flexGrow: 1 }}>
                    <Grid container spacing={2}>
                        <Grid item xs={6} md={8}>
                            <Paper elevation={2}>
                                <Typography component="h3" variant="h5">Posts</Typography>
                            </Paper>
                        </Grid>
                        <Grid item xs={6} md={4}>
                            <Paper elevation={2}>
                                <Typography component="h3" variant="h5">Users</Typography>
                            </Paper>
                        </Grid>
                    </Grid>
            </Box>
        </Layout>
    );
};

export default Home;