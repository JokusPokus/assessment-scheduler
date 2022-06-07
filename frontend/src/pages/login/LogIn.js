import React, { useState, useEffect } from "react";
import { Button, Layout, Form, Input, message } from "antd";
import { useNavigate } from "react-router-dom";
import { Content } from "antd/lib/layout/layout";
import "./login.css"

const { Header } = Layout;

const LogIn = ({ requestUrl, setUserInfo }) => {
    const navigate = useNavigate();
    const [loginUser, setLoginUser] = useState(undefined);

    const onFinish = (values) => {
        setLoginUser({
            'username': values.email,
            'password': values.password
        });
    };

    useEffect(async () => {
        if(loginUser) {
            const requestOptions = {
                method: 'POST',
                headers : {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(loginUser)
            };

            const loginResponse = fetch(`${requestUrl}/auth/token/`, requestOptions)
                .then(response => {
                    if(response.status === 200) {
                        return response.json()
                    } else {
                        message.warning('Email and/or password is wrong.')
                    }
                });

            const setCookie = async () => {
                const tokens = await loginResponse;
                if(tokens) {
                    window.localStorage.setItem('access', tokens.access);
                    window.localStorage.setItem('refresh', tokens.refresh);
                    console.log('Access and refresh tokens set');
                    message.success(`Welcome, ${loginUser.username}!`);
                    navigate('/portal');
                }
            };

            await setCookie();
        }
    }, [loginUser, requestUrl, navigate]);

    const onFinishFailed = (errorInfo) => {
        message.warning(`There has been a problem: ${errorInfo}`)
    };

    return(
        <Layout
            className="site-layout-background"
            style={{
                height: "100%"
            }}
        >
            <Layout
                style={{
                    backgroundImage: `url(/landing-page.jpg)`,
                    backgroundSize: "cover",
                    justifyContent: "center",
                    alignItems: "center"
                }}
            >
                <Content style={{
                    margin: 'auto',
                    padding: '50px 50px',
                    width: '30%',
                    backgroundColor: 'white',
                    borderRadius: '4px',
                    boxShadow: 'rgba(0, 0, 0, 0.8) 12px 12px 12px',
                    flex: '0 1 auto'
                }}>
                    <div className='page_content'>
                        <div className='left_col'>
                            <div
                                className='greet'
                                style={{
                                    marginTop: '10px',
                                    marginBottom: '20px',
                                    fontFamily: "'Source Sans Pro', sans-serif",
                                    fontSize: '2rem'
                                }}
                            >
                                <p className='sign_up'>CODE Assessment Scheduler</p>
                            </div>
                        </div>
                        <div className='right_col'>
                            <Form
                                name="basic"
                                wrapperCol={{
                                    span: 24,
                                }}
                                initialValues={{
                                    remember: true,
                                }}
                                onFinish={onFinish}
                                onFinishFailed={onFinishFailed}
                                autoComplete="on"
                                size="large"
                            >

                                <Form.Item
                                    name="email"
                                >
                                    <Input placeholder="E-mail" />
                                </Form.Item>

                                <Form.Item
                                    name="password"
                                >
                                    <Input.Password placeholder="Password"/>
                                </Form.Item>

                                <Form.Item
                                    wrapperCol={{
                                    offset: 0,
                                    span: 24,
                                    }}>
                                    <Button block type="primary" htmlType="submit">
                                        Log In
                                    </Button>
                                </Form.Item>
                            </Form>
                        </div>
                    </div>
                </Content>
            </Layout>
        </Layout>
    )
};

export default LogIn;