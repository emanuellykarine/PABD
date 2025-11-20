import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

function DashCliente() {
    const [username, setUsername] = useState('');
    const navigate = useNavigate();

    useEffect(() => {
        // Busca informações do usuário logado
        const fetchUserData = async () => {
            const token = localStorage.getItem('token');
            
            if (!token) {
                navigate('/login');
                return;
            }

            try {
                const response = await fetch('http://localhost:8000/auth/perfil/', {
                    headers: {
                        'Authorization': `Token ${token}`,
                        'Content-Type': 'application/json'
                    }
                });

                if (response.ok) {
                    const data = await response.json();
                    setUsername(data.username);
                } else {
                    // Token inválido ou expirado
                    localStorage.removeItem('token');
                    navigate('/login');
                }
            } catch (error) {
                console.error('Erro ao buscar dados do usuário:', error);
                navigate('/login');
            }
        };

        fetchUserData();
    }, [navigate]);

    const handleLogout = async () => {
        const token = localStorage.getItem('token');

        try {
            // Chama o endpoint de logout no backend
            await fetch('http://localhost:8000/auth/logout/', {
                method: 'POST',
                headers: {
                    'Authorization': `Token ${token}`,
                    'Content-Type': 'application/json'
                }
            });
        } catch (error) {
            console.error('Erro ao fazer logout:', error);
        } finally {
            // Remove o token do localStorage independente do resultado
            localStorage.removeItem('token');
            // Redireciona para a página de login
            navigate('/login');
        }
    };
    
    return (
        <div>
            <h1>Dashboard do Cliente</h1>
            {username && <p>Bem-vindo, {username}!</p>}
            <button onClick={handleLogout}>Sair</button>
        </div>
    );
}

export default DashCliente;