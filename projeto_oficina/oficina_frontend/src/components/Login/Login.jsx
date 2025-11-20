import { useState } from 'react';
import './Login.css';
import { useNavigate } from 'react-router-dom';

function Login() {
    const [formData, setFormData] = useState({
        username: '',
        password: ''
    });

    const [error, setError] = useState('');
    const [success, setSuccess] = useState('');
    const navigate = useNavigate(); // HOOK DE NAVEGAÇÃO


    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData(prev => ({ // Mantém os valores anteriores
            ...prev,
            [name]: value
        }));
    }

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        setSuccess('');

        if (!formData.username || !formData.password) {
            setError('Por favor, preencha todos os campos.');
            return;
        }

        try {
            const response = await fetch('http://localhost:8000/auth/login/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData)
            });

            if (response.ok) {
                const data = await response.json();
                setSuccess('Login bem-sucedido!');
                
                if (data.token) {
                    localStorage.setItem('token', data.token);
                }

                if (data.tipo_perfil === 'CLIENTE') {
                    navigate('/dashboard/cliente');
                } else if (data.tipo_perfil === 'MECANICO') {
                    navigate('/dashboard/mecanico');
                } else if (data.tipo_perfil === 'GERENTE') {
                    navigate('/dashboard/gerente');
                } else {
                    // Fallback para perfis não mapeados
                    navigate('/dashboard/cliente');
                }
            } else {
                const errorData = await response.json();
                setError(errorData.detail || 'Erro no login. Verifique suas credenciais.');
            }
        } catch (err) {
            setError('Erro ao conectar ao servidor. Tente novamente mais tarde.');
            console.error('Erro de conexão:', err);
        }
    };

    return (
        <div className="login-container">
            <h2>Login de Usuário</h2>
            <form onSubmit={handleSubmit}>
                <div className="form-group">
                    <label htmlFor="username">Nome de usuário</label>
                    <input type="text"
                        id="username"
                        name="username"
                        value={formData.username}
                        onChange={handleChange}
                        required />
                </div>

                <div className="form-group">
                    <label htmlFor="password">Senha</label>
                    <input type="password"
                        id="password"
                        name="password"
                        value={formData.senha}
                        onChange={handleChange}
                        required />
                </div>

                {error && <div className="error-message">{error}</div>}
                {success && <div className="success-message">{success}</div>}

                <button type="submit">Entrar</button>
            </form>
        </div>
    )
}

export default Login;