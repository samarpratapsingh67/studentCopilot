import { useState } from 'react';
import PredictionForm from '../components/PredictionForm';
import ResultCard from '../components/ResultCard';
import Card from '../components/Card';
import { predictCustomer } from '../services/api';

const Predict = () => {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');

  const handleSubmit = async (payload) => {
    setLoading(true);
    setError('');

    try {
      const prediction = await predictCustomer(payload);
      setResult(prediction);
    } catch (err) {
      const message =
        err?.response?.data?.error || err?.message || 'Prediction failed. Please check the API and try again.';
      setError(message);
      setResult(null);
    } finally {
      setLoading(false);
    }
  };

  return (
    <section className="space-y-6">
      <div className="glass-card animate-fadeUp rounded-2xl p-6">
        <p className="text-sm uppercase tracking-[0.22em] text-mint">Real-time scoring</p>
        <h2 className="mt-2 text-2xl font-semibold text-white sm:text-3xl">Customer Churn Prediction</h2>
        <p className="mt-3 max-w-3xl text-slate-300">
          Enter customer details and get an instant churn risk score. Use the segment label to prioritize retention
          outreach.
        </p>
      </div>

      {error && (
        <Card className="border-rose-500/40 bg-rose-950/20" title="API Error">
          <p className="text-sm text-rose-200">{error}</p>
        </Card>
      )}

      <div className="grid grid-cols-1 gap-4 xl:grid-cols-[1.2fr_0.8fr]">
        <Card title="Customer Inputs" subtitle="All fields are required.">
          <PredictionForm onSubmit={handleSubmit} loading={loading} />
        </Card>
        <ResultCard result={result} />
      </div>
    </section>
  );
};

export default Predict;
