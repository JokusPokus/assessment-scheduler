import React, { useState, useEffect } from "react";
import { Button, Layout, Form, Input, message } from "antd";
import { useNavigate } from "react-router-dom";
import { Content } from "antd/lib/layout/layout";

const { Header } = Layout;

const LogIn = ({ requestUrl }) => {
    const [loginUser, setLoginUser] = useState(undefined);
    const navigate = useNavigate();

    const onFinish = (values) => {
        setLoginUser({
            'username': values.email,
            'password': values.password
        });
        navigate('/portal');
    };

    useEffect(() => {
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
                    navigate('/portal')
                }
            };

            setCookie()
        }
    }, [loginUser, requestUrl, navigate]);

    /////// Any? //////
    const onFinishFailed = (errorInfo) => {

    };

    return(
        <Layout className="site-layout-background">
            <Header className="header navbar-layout-background" >
                <div className='navbar-content'>
                </div>
            </Header>
            <Layout>
                <Content style={{ width: '30%', margin: 'auto', padding: '50px 50px', background: '#fff'}}>
                    <div className='page_content'>
                        <div className='left_col'>
                            <div className='greet'>
                                <p className='sign_up'>Sign In to get started!</p>
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
                                autoComplete="off" >

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