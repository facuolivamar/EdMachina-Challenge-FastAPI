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
        const personaRes = await axios.post('http://localhost:8000/persona', values.persona);
        personaId = personaRes.data.id;
      }

      if (showMateriaForm) {
        const materiaRes = await axios.post('http://localhost:8000/materia', values.materia);
        materiaId = materiaRes.data.id;
      }

      if (showCarreraForm) {
        const carreraRes = await axios.post('http://localhost:8000/carrera', values.carrera);
        carreraId = carreraRes.data.id;
      }

      const registroData = {
        ...values,
        persona_id: personaId,
        materia_id: materiaId,
        carrera_id: carreraId,
        calificacion_final: Number(values.calificacion_final), // Asegúrate de convertirlo a número
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
    } catch (error) {
      message.error('Failed to create Registro');
    }
  };

  return (
    <Form form={form} onFinish={onFinish} layout="vertical">
      <Form.Item
        name="calificacion_final"
        label="Calificación Final"
        rules={[{ min: 0, max: 10 }]}
      >
        <Input type="number" step="0.1" />
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
          <Form.Item name={['persona', 'numero_dni_persona']} rules={[{ required: true, type: 'number', min: 1 }]}>
            <Input type="number" placeholder="DNI" />
          </Form.Item>
          <Form.Item name={['persona', 'fecha_nacimiento_persona']} rules={[{ required: true }]}>
            <DatePicker placeholder="Fecha de Nacimiento" />
          </Form.Item>
          <Form.Item name={['persona', 'direccion_persona']} rules={[{ required: true, min: 1 }]}>
            <Input placeholder="Dirección" />
          </Form.Item>
          <Form.Item name={['persona', 'telefono_persona']} rules={[{ required: true, type: 'number', min: 1 }]}>
            <Input type="number" placeholder="Teléfono" />
          </Form.Item>
          <Form.Item name={['persona', 'anio_inscripcion_persona']} rules={[{ required: true, type: 'number', min: 1 }]}>
            <Input type="number" placeholder="Año de Inscripción" />
          </Form.Item>
        </Form.Item>
      )}

      <Form.Item name="materia_id" label="Materia" rules={[{ required: true }]}>
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

      {showMateriaForm && (
        <Form.Item label="New Materia">
          <Form.Item name={['materia', 'nombre_materia']} rules={[{ required: true, min: 1 }]}>
            <Input placeholder="Nombre de Materia" />
          </Form.Item>
          <Form.Item name={['materia', 'anio_materia']} rules={[{ required: true, min: 1 }]}>
            <Input type="number" placeholder="Año de Materia" />
          </Form.Item>
        </Form.Item>
      )}

      <Form.Item name="carrera_id" label="Carrera" rules={[{ required: true }]}>
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

      {showCarreraForm && (
        <Form.Item label="New Carrera">
          <Form.Item name={['carrera', 'nombre_carrera']} rules={[{ required: true, min: 1 }]}>
            <Input placeholder="Nombre de Carrera" />
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