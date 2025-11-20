import { useState } from 'react';
import './Registro.css';

function Registro() {
    const [formData, setFormData] = useState({
        username: '',
        email: '',
        cpf: '',
        telefone: '',
        tipo_perfil: '',
        senha: '',
        confirmar_senha: ''
    });

    const [error, setError] = useState('');
    const [success, setSuccess] = useState('');

    const perfis = [
        { value: 'GERENTE', label: 'Gerente' },
        { value: 'CLIENTE', label: 'Cliente' },
        { value: 'MECANICO', label: 'Mecânico' },
        { value: 'ADMIN', label: 'Administrador' }
    ]

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData(prev => ({ // Mantém os valores anteriores
            ...prev,
            [name]: value
        }));
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        setSuccess('');

        if (formData.senha !== formData.confirmar_senha) {
            setError('As senhas não coincidem.');
            return;
        }

        if (!formData.username || !formData.email || !formData.cpf || !formData.telefone || !formData.tipo_perfil || !formData.senha) {
            setError('Por favor, preencha todos os campos.');
            return;
        }

        try {
            const response = await fetch('http://localhost:8000/auth/registro/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(formData)
        });

            if (response.ok) {
                const data = await response.json();
                setSuccess('Registro bem-sucedido! Você pode fazer login agora.');
                setFormData({
                    username: '',
                    email: '',
                    cpf: '',
                    telefone: '',
                    tipo_perfil: '',
                    senha: '',
                    confirmar_senha: ''
                });
                navigate('/auth/login');
            } else {
                const errorData = await response.json();
                setError(errorData.detail || 'Erro no registro. Tente novamente.');
            }
        } catch (error) {
            setError('Erro na conexão com o servidor. Tente novamente mais tarde.');
        }
    };

    return (
        <div className="registro-container">
            <h2>Registro de Usuário</h2>
            <form onSubmit={handleSubmit}>

                <div className='form-group'>
                    <label htmlFor="username">Nome de usuário</label>
                    <input type="text"
                    name="username"
                    id ="username"
                    value={formData.username}
                    onChange={handleChange}
                    required
                    />
                </div>

                <div className='form-group'>
                    <label htmlFor="email">Email</label>
                    <input type="email"
                    name="email"
                    id ="email"
                    value={formData.email}
                    onChange={handleChange}
                    required
                    />
                </div>

                <div className='form-group'>
                    <label htmlFor="cpf">CPF</label>
                    <input type="text"
                    name="cpf"
                    id ="cpf"
                    value={formData.cpf}
                    onChange={handleChange}
                    required
                    />
                </div>

                <div className='form-group'>
                    <label htmlFor="telefone">Telefone</label>
                    <input type="text"
                    name="telefone"
                    id ="telefone"
                    value={formData.telefone}
                    onChange={handleChange}
                    required
                    />
                </div>

                <div className='form-group'>
                    <label htmlFor="tipo_perfil">Tipo de Perfil</label>
                    <select
                    name="tipo_perfil"
                    id="tipo_perfil"
                    value={formData.tipo_perfil}
                    onChange={handleChange}
                    required
                    >
                        <option value="">Selecione um tipo</option>
                        {perfis.map(option => (
                            <option key={option.value} value={option.value}>
                                {option.label}
                            </option>
                        ))}
                    </select>
                </div>

                <div className='form-group'>
                    <label htmlFor="senha">Senha</label>
                    <input
                    type="password"
                    name="senha"
                    id="senha"
                    value={formData.senha}
                    onChange={handleChange}
                    required
                    />
                </div>

                <div className='form-group'>
                    <label htmlFor="confirmar_senha">Confirmar Senha</label>
                    <input
                    type="password"
                    name="confirmar_senha"
                    id="confirmar_senha"
                    value={formData.confirmar_senha}
                    onChange={handleChange}
                    required
                    />
                </div>

                <button type="submit">Registrar</button>

                {error && <p className="error-message">{error}</p>}
                {success && <p className="success-message">{success}</p>}

            </form>
        </div>
    )

}

export default Registro;
