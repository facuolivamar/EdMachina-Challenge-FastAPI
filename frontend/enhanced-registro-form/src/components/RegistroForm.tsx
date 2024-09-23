import React, { useState, useEffect } from 'react';
import { Button, Form, Select, Input, DatePicker, Checkbox, message } from 'antd';
import axios from 'axios';

const { Option } = Select;

interface Persona {
  id: number;
  nombre_persona: string;
  apellido_persona: string;
  email_persona: string;
  numero_dni_persona: number;
  fecha_nacimiento_persona: string;
  direccion_persona: string;
  telefono_persona: number;
  anio_inscripcion_persona: number;
}

interface Materia {
  id: number;
  nombre_materia: string;
  anio_materia: number;
}

interface Carrera {
  id: number;
  nombre_carrera: string;
}

const RegistroForm: React.FC = () => {
  const [form] = Form.useForm();
  const [personas, setPersonas] = useState<Persona[]>([]);
  const [materias, setMaterias] = useState<Materia[]>([]);
  const [carreras, setCarreras] = useState<Carrera[]>([]);
  const [showPersonaForm, setShowPersonaForm] = useState(false);
  const [showMateriaForm, setShowMateriaForm] = useState(false);
  const [showCarreraForm, setShowCarreraForm] = useState(false);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const [personasRes, materiasRes, carrerasRes] = await Promise.all([
        axios.get<Persona[]>('http://localhost:8000/persona'),
        axios.get<Materia[]>('http://localhost:8000/materia'),
        axios.get<Carrera[]>('http://localhost:8000/carrera'),
      ]);
      setPersonas(personasRes.data);
      setMaterias(materiasRes.data);
      setCarreras(carrerasRes.data);
    } catch (error) {
      message.error('Failed to fetch data');
    }
  };

  const onFinish = async (values: any) => {
    try {
      let personaId = values.persona_id;
      let materiaId = values.materia_id;
      let carreraId = values.carrera_id;

      if (showPersonaForm) {
        const personaData = {
          ...values.persona,
          telefono_persona: Number(values.persona.telefono_persona),
          numero_dni_persona: Number(values.persona.numero_dni_persona),
          anio_inscripcion_persona: Number(values.persona.anio_inscripcion_persona),
          fecha_nacimiento_persona: values.persona.fecha_nacimiento_persona.format('YYYY-MM-DD'),
        };

        console.log(personaData);
        const personaRes = await axios.post('http://localhost:8000/persona', personaData);
        personaId = personaRes.data.id;
  
        // Actualizar el valor del campo de selección
        form.setFieldsValue({ persona_id: personaId });
        setShowPersonaForm(false);
      }

      if (showMateriaForm) {
        const materiaRes = await axios.post('http://localhost:8000/materia', values.materia);
        materiaId = materiaRes.data.id;
  
        // Actualizar el valor del campo de selección
        form.setFieldsValue({ materia_id: materiaId });
        setShowMateriaForm(false);
      }

      if (showCarreraForm) {
        const carreraRes = await axios.post('http://localhost:8000/carrera', values.carrera);
        carreraId = carreraRes.data.id;
  
        // Actualizar el valor del campo de selección
        form.setFieldsValue({ carrera_id: carreraId });
        setShowCarreraForm(false);
      }

      const registroData = {
        ...values,
        persona_id: personaId,
        materia_id: materiaId,
        carrera_id: carreraId,
        calificacion_final: Number(values.calificacion_final),
        fecha_inicio_cursado: values.fecha_inicio_cursado ? values.fecha_inicio_cursado.format('YYYY-MM-DD') : null,
        fecha_fin_cursado: values.fecha_fin_cursado ? values.fecha_fin_cursado.format('YYYY-MM-DD') : null,
        activo: values.activo !== undefined ? values.activo : null,
      };
      console.log("registroData: ", registroData);

      await axios.post('http://localhost:8000/registro', registroData);
      message.success('Registro created successfully');
      form.resetFields();
      setShowPersonaForm(false);
      setShowMateriaForm(false);
      setShowCarreraForm(false);
      fetchData();
    } catch (error: any) {
    // Captura de error
    if (error.response && error.response.status === 422) {
      const errorMessage = error.response.data.detail;
     
      message.error(errorMessage);

      // Opcional: Si hay campos específicos que han causado el error, se pueden marcar como errores en el formulario.
      if (errorMessage.includes('email')) {
        form.setFields([
          {
            name: ['persona', 'email_persona'],
            errors: [errorMessage], // Mostrar el mensaje exacto del backend
          },
        ]);
      }
      if (errorMessage.includes('numero_dni_persona')) {
        form.setFields([
          {
            name: ['persona', 'numero_dni_persona'],
            errors: [errorMessage], // Mostrar el mensaje exacto del backend
          },
        ]);
      }
      // Agrega más condiciones si el backend devuelve otros mensajes específicos
    } else {
      message.error('Error en la solicitud. Inténtalo de nuevo.');
    }
  }
  };

  return (
    <Form form={form} onFinish={onFinish} layout="vertical">
      <Form.Item
        name="calificacion_final"
        label="Calificación Final"
      >
        <Input type="number" step="0.1" min={0.1} max={10}/>
      </Form.Item>

      <Form.Item
        name="fecha_inicio_cursado"
        label="Fecha Inicio Cursado"
        rules={[{ required: true }]}
      >
        <DatePicker />
      </Form.Item>

      <Form.Item name="fecha_fin_cursado" label="Fecha Fin Cursado">
        <DatePicker />
      </Form.Item>

      <Form.Item name="activo" valuePropName="checked">
        <Checkbox>Activo</Checkbox>
      </Form.Item>

      {!showPersonaForm && (
        <Form.Item name="persona_id" label="Persona" rules={[{ required: true }]}>
        <Select
          onChange={(value) => setShowPersonaForm(value === 'new')}
          dropdownRender={(menu) => (
            <>
              {menu}
              <Button type="link" onClick={() => setShowPersonaForm(true)}>
                Add New Persona
              </Button>
            </>
          )}
        >
          {personas.map((persona) => (
            <Option key={persona.id} value={persona.id}>
              {`${persona.nombre_persona} ${persona.apellido_persona} (DNI: ${persona.numero_dni_persona})`}
            </Option>
          ))}
        </Select>
      </Form.Item>
      )}

      {showPersonaForm && (
        <Form.Item label="New Persona">
          <Form.Item name={['persona', 'nombre_persona']} rules={[{ required: true, min: 1 }]}>
            <Input placeholder="Nombre" />
          </Form.Item>
          <Form.Item name={['persona', 'apellido_persona']} rules={[{ required: true, min: 1 }]}>
            <Input placeholder="Apellido" />
          </Form.Item>
          <Form.Item name={['persona', 'email_persona']} rules={[{ required: true, type: 'email', min: 3 }]}>
            <Input placeholder="Email" />
          </Form.Item>
          <Form.Item name={['persona', 'numero_dni_persona']} rules={[{ required: true, min: 1 }]}>
            <Input type="number" min={1} placeholder="DNI" />
          </Form.Item>
          <Form.Item name={['persona', 'fecha_nacimiento_persona']} rules={[{ required: true }]}>
            <DatePicker placeholder="Fecha de Nacimiento" />
          </Form.Item>
          <Form.Item name={['persona', 'direccion_persona']} rules={[{ required: true, min: 1 }]}>
            <Input placeholder="Dirección" />
          </Form.Item>
          <Form.Item name={['persona', 'telefono_persona']} rules={[{ required: true, min: 1 }]}>
            <Input type="number" min={1} placeholder="Teléfono" />
          </Form.Item>
          <Form.Item name={['persona', 'anio_inscripcion_persona']} rules={[{ required: true, min: 1 }]}>
            <Input type="number" min={1} placeholder="Año de Inscripción" />
          </Form.Item>
          <Form.Item>
            <Button type="link" onClick={() => setShowPersonaForm(false)}>
              Cancelar
            </Button>
          </Form.Item>
        </Form.Item>
      )}

      {!showMateriaForm && (<Form.Item
        name="materia_id"
        label="Materia"
        rules={[{ required: !showMateriaForm }]} // Deshabilitar validación si se está creando una nueva materia
        >
          <Select
            onChange={(value) => setShowMateriaForm(value === 'new')}
            dropdownRender={(menu) => (
              <>
                {menu}
                <Button type="link" onClick={() => setShowMateriaForm(true)}>
                  Add New Materia
                </Button>
              </>
            )}
          >
            {materias.map((materia) => (
              <Option key={materia.id} value={materia.id}>
                {`${materia.nombre_materia} (Year: ${materia.anio_materia})`}
              </Option>
            ))}
          </Select>
        </Form.Item>
      )}

      {showMateriaForm && (
        <Form.Item label="New Materia">
          <Form.Item name={['materia', 'nombre_materia']} rules={[{ required: true}]}>
            <Input placeholder="Nombre de Materia" />
          </Form.Item>
          <Form.Item name={['materia', 'anio_materia']} rules={[{ required: true }]}>
            <Input type="number" step="1" min={1} placeholder="Año de Materia" />
          </Form.Item>
          <Form.Item>
            <Button type="link" onClick={() => setShowMateriaForm(false)}>
              Cancelar
            </Button>
          </Form.Item>

        </Form.Item>
        
      )}

      {!showCarreraForm && (
        <Form.Item name="carrera_id" label="Carrera" rules={[{ required: !showCarreraForm }]}>
          <Select
            onChange={(value) => setShowCarreraForm(value === 'new')}
            dropdownRender={(menu) => (
              <>
                {menu}
                <Button type="link" onClick={() => setShowCarreraForm(true)}>
                  Add New Carrera
                </Button>
              </>
            )}
          >
            {carreras.map((carrera) => (
              <Option key={carrera.id} value={carrera.id}>
                {carrera.nombre_carrera}
              </Option>
            ))}
          </Select>
        </Form.Item>
      )}

      {showCarreraForm && (
        <Form.Item label="New Carrera">
          <Form.Item name={['carrera', 'nombre_carrera']} rules={[{ required: true, min: 1 }]}>
            <Input placeholder="Nombre de Carrera" />
          </Form.Item>
          <Form.Item>
            <Button type="link" onClick={() => setShowCarreraForm(false)}>
              Cancelar
            </Button>
          </Form.Item>
        </Form.Item>
      )}

      <Form.Item>
        <Button type="primary" htmlType="submit">
          Submit
        </Button>
      </Form.Item>
    </Form>
  );
};

export default RegistroForm;