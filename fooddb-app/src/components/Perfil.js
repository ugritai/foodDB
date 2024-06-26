import React, { useContext } from 'react';
import AuthContext from '../Auth';

const languageMap = {
    EN: 'English',
    ES: 'Español'
};

const cuisineMap = {
    PAN: 'Panamá',
    ARG: 'Argentina',
    VEN: 'Venezuela',
    URY: 'Uruguay',
    SLV: 'El Salvador',
    PRI: 'Puerto Rico',
    CHL: 'Chile',
    CRI: 'Costa Rica',
    NIC: 'Nicaragua',
    MEX: 'México',
    DOM: 'República Dominicana',
    HND: 'Honduras',
    COL: 'Colombia',
    ESP: 'España',
    GTM: 'Guatemala',
    PER: 'Perú',
    PRY: 'Paraguay',
    ECU: 'Ecuador',
    BOL: 'Bolivia',
    CUB: 'Cuba'
};

const Perfil = () => {
    const { isAuthenticated, user } = useContext(AuthContext);


    if (!isAuthenticated) {
        return <p>No estás autenticado. Por favor, inicia sesión.</p>;
    }

    if (!user) {
        return <p>Cargando información del usuario...</p>;
    }

    const idiomas = user.preferences?.languages || [];

    // Función para obtener el mensaje del nivel de actividad
    const getActivityMessage = () => {

        if (idiomas.length === 1 && idiomas[0] === 'EN'){
            if (user.activity_level === 1) {
                return "Not very active. Predominantly sedentary activity, with little physical activity.";
            } else if (user.activity_level === 2) {
                return "Moderately active. Occasional participation in activities that require standing or light movements.";
            } else if (user.activity_level === 3) {
                return "Active. Involved in activities that include walking or regular household tasks.";
            } else if (user.activity_level === 4) {
                return "Very active. Participation in intense physical activities, such as sports or physical work.";
            } else {
                return "Inactive.";
            }
        } else{

            
            if (user.activity_level === 1) {
                return "No muy activo. Actividad predominantemente sedentaria, con poca actividad física.";
            } else if (user.activity_level === 2) {
                return "Medianamente activo. Participación ocasional en actividades que requieren estar de pie o movimientos ligeros.";
            } else if (user.activity_level === 3) {
                return "Activo. Involucrado en actividades que incluyen caminar o realizar tareas domésticas regulares.";
            } else if (user.activity_level === 4) {
                return "Muy activo. Participación en actividades físicas intensas, como deportes o trabajo físico.";
            } else {
                return "Inactivo.";
            }
        }
    };

    const getGenero = () => {
        if (idiomas.length === 1 && idiomas[0] === 'EN') {
            if (user.gender === 'Hombre'){
                return 'Male'
            } else {
                return 'Female'
            }
        }

        return user.gender;
    }

    return (
        <div className='cell perfil'>
            <h2>
            {idiomas.length === 1 && idiomas[0] === 'EN' 
                ? `${user.name}'s profile` 
                : `Perfil de ${user.name}`}
            </h2>
            <p><strong>Email:</strong> {user.email}</p>
            {user.gender && <p><strong>{ idiomas.length === 1 && idiomas[0] === 'EN' ? 'Gender' : 'Género'}: </strong>{getGenero()}</p>}
            {user.age > 0 && <p><strong>{ idiomas.length === 1 && idiomas[0] === 'EN' ? 'Age' : 'Edad'}: </strong>{user.age}</p>}
            {user.height > 0 && <p><strong> { idiomas.length === 1 && idiomas[0] === 'EN' ? 'Height' : 'Altura'}: </strong>{user.height} cm</p>}
            {user.weight > 0 && <p><strong> { idiomas.length === 1 && idiomas[0] === 'EN' ? 'Weight' : 'Peso'}: </strong>{user.weight} kg</p>}
            {user.activity_level > 0 && <p><strong> { idiomas.length === 1 && idiomas[0] === 'EN' ? 'Activity level' : 'Nivel de actividad'}: </strong>{getActivityMessage()}</p>}
            {user.daily_caloric_intake > 0 && <p><strong> { idiomas.length === 1 && idiomas[0] === 'EN' ? 'Daily caloric intake' : 'Ingesta calórica diaria'}: </strong>{user.daily_caloric_intake} kcal</p>}
            
            {/* Mostrar restricciones en una tabla si la ingesta calórica diaria recomendada es mayor que 0 */}
            {user.daily_caloric_intake > 0 && (
                <div>
                    <h3> { idiomas.length === 1 && idiomas[0] === 'EN' ? 'Nutritional restrictions' : 'Restricciones nutricionales'}</h3>
                    <table className="restricciones-tabla">
                        <thead>
                            <tr>
                                <th> { idiomas.length === 1 && idiomas[0] === 'EN' ? 'Nutrient' : 'Nutriente'}</th>
                                <th> { idiomas.length === 1 && idiomas[0] === 'EN' ? 'Calories (kcal)' : 'Calorías (kcal)'}</th>
                                <th> { idiomas.length === 1 && idiomas[0] === 'EN' ? 'Grams (g)' : 'Gramos (g)'}</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td> { idiomas.length === 1 && idiomas[0] === 'EN' ? 'Proteins' : 'Proteínas'}</td>
                                <td>{user.restrictions_kcal?.fats?.total || '-'}</td>
                                <td>{user.restrictions_grams?.fats?.total || '0'}</td>
                            </tr>
                            <tr>
                                <td> { idiomas.length === 1 && idiomas[0] === 'EN' ? 'Fats' : 'Grasas'}</td>
                                <td>{user.restrictions_kcal?.fats?.sat || '-'}</td>
                                <td>{user.restrictions_grams?.fats?.sat || '0'}</td>
                            </tr>
                            <tr>
                                <td> { idiomas.length === 1 && idiomas[0] === 'EN' ? 'Saturated fats' : 'Grasas saturadas'}</td>
                                <td>{user.restrictions_kcal?.fats?.trans || '-'}</td>
                                <td>{user.restrictions_grams?.fats?.trans || '0'}</td>
                            </tr>
                            <tr>
                                <td> { idiomas.length === 1 && idiomas[0] === 'EN' ? 'Sugars' : 'Azúcares'}</td>
                                <td>{user.restrictions_kcal?.sugars || '-'}</td>
                                <td>{user.restrictions_grams?.sugars || '0'}</td>
                            </tr>
                            <tr>
                                <td> { idiomas.length === 1 && idiomas[0] === 'EN' ? 'Sodium' : 'Sodio'}</td>
                                <td>-</td>
                                <td>{user.restrictions_grams?.sodium || '0'}</td>
                            </tr>
                            <tr>
                                <td> { idiomas.length === 1 && idiomas[0] === 'EN' ? 'Salt' : 'Sal'}</td>
                                <td>-</td>
                                <td>{user.restrictions_grams?.salt || '0'}</td>
                            </tr>
                            <tr>
                                <td> { idiomas.length === 1 && idiomas[0] === 'EN' ? 'Potassium' : 'Potasio'}</td>
                                <td>-</td>
                                <td>{user.restrictions_grams?.potassium || '0'}</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            )}

            {/* Mostrar preferencias de idiomas si el array no está vacío */}
            {user.preferences?.languages?.length > 0 && (
                <div className='listado-idiomas-gastro'>
                    <h3> { idiomas.length === 1 && idiomas[0] === 'EN' ? 'Preferred languages' : 'Idiomas preferidos'}</h3>
                    <ul>
                        {user.preferences.languages.map((language, index) => (
                            <li key={index}>{languageMap[language]}</li>
                        ))}
                    </ul>
                </div>
            )}

            {/* Mostrar preferencias de gastronomía si el array no está vacío */}
            {user.preferences?.cuisines?.length > 0 && (
                <div className='listado-idiomas-gastro'>
                    <h3>Gastronomías preferidas</h3>
                    <ul>
                        {user.preferences.cuisines.map((cuisine, index) => (
                            <li key={index}>{cuisineMap[cuisine]}</li>
                        ))}
                    </ul>
                </div>
            )}
        </div>
    );
};

export default Perfil;
