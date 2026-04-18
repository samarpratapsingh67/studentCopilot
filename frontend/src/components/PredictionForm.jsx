import { useMemo, useState } from 'react';

const initialFormState = {
  age: '',
  gender: 'Male',
  subscription_type: 'Standard',
  watch_hours: '',
  last_login_days: '',
  region: 'Europe',
  device: 'Mobile',
  monthly_fee: '',
  payment_method: 'Credit Card',
  number_of_profiles: '2',
  avg_watch_time_per_day: '',
  favorite_genre: 'Drama',
};

const PredictionForm = ({ onSubmit, loading }) => {
  const [formData, setFormData] = useState(initialFormState);

  const fields = useMemo(
    () => [
      { key: 'age', label: 'Age', type: 'number', min: 18, max: 100 },
      {
        key: 'gender',
        label: 'Gender',
        type: 'select',
        options: ['Male', 'Female'],
      },
      {
        key: 'subscription_type',
        label: 'Subscription Type',
        type: 'select',
        options: ['Basic', 'Standard', 'Premium'],
      },
      { key: 'watch_hours', label: 'Watch Hours (Monthly)', type: 'number', min: 0, step: '0.1' },
      { key: 'last_login_days', label: 'Days Since Last Login', type: 'number', min: 0, max: 365 },
      {
        key: 'region',
        label: 'Region',
        type: 'select',
        options: ['North America', 'Europe', 'Asia', 'South America'],
      },
      {
        key: 'device',
        label: 'Primary Device',
        type: 'select',
        options: ['Mobile', 'Desktop', 'Tablet', 'TV'],
      },
      { key: 'monthly_fee', label: 'Monthly Fee', type: 'number', min: 0, step: '0.01' },
      {
        key: 'payment_method',
        label: 'Payment Method',
        type: 'select',
        options: ['Credit Card', 'Debit Card', 'PayPal', 'Bank Transfer'],
      },
      {
        key: 'number_of_profiles',
        label: 'Number of Profiles',
        type: 'number',
        min: 1,
        max: 5,
      },
      {
        key: 'avg_watch_time_per_day',
        label: 'Avg Watch Time / Day (Hours)',
        type: 'number',
        min: 0,
        step: '0.1',
      },
      {
        key: 'favorite_genre',
        label: 'Favorite Genre',
        type: 'select',
        options: ['Drama', 'Action', 'Comedy', 'Thriller', 'Documentary'],
      },
    ],
    []
  );

  const handleChange = (event) => {
    const { name, value } = event.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSubmit = (event) => {
    event.preventDefault();

    onSubmit({
      ...formData,
      age: Number(formData.age),
      watch_hours: Number(formData.watch_hours),
      last_login_days: Number(formData.last_login_days),
      monthly_fee: Number(formData.monthly_fee),
      number_of_profiles: Number(formData.number_of_profiles),
      avg_watch_time_per_day: Number(formData.avg_watch_time_per_day),
    });
  };

  const handleReset = () => {
    setFormData(initialFormState);
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-5">
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
        {fields.map((field) => {
          const value = formData[field.key];

          return (
            <div key={field.key}>
              <label className="input-label" htmlFor={field.key}>
                {field.label}
              </label>

              {field.type === 'select' ? (
                <select
                  id={field.key}
                  name={field.key}
                  value={value}
                  onChange={handleChange}
                  className="input-control"
                  required
                >
                  {field.options.map((option) => {
                    if (typeof option === 'string') {
                      return (
                        <option key={option} value={option}>
                          {option}
                        </option>
                      );
                    }

                    return (
                      <option key={option.value} value={option.value}>
                        {option.label}
                      </option>
                    );
                  })}
                </select>
              ) : (
                <input
                  id={field.key}
                  name={field.key}
                  type="number"
                  value={value}
                  onChange={handleChange}
                  className="input-control"
                  min={field.min}
                  max={field.max}
                  step={field.step || 1}
                  required
                />
              )}
            </div>
          );
        })}
      </div>

      <div className="flex flex-col gap-3 sm:flex-row">
        <button type="submit" className="primary-btn w-full sm:w-auto" disabled={loading}>
          {loading ? (
            <span className="inline-flex items-center gap-2">
              <span className="h-4 w-4 animate-spin rounded-full border-2 border-slate-900 border-t-transparent" />
              Predicting...
            </span>
          ) : (
            'Predict Churn Risk'
          )}
        </button>
        <button type="button" className="secondary-btn w-full sm:w-auto" onClick={handleReset}>
          Reset
        </button>
      </div>
    </form>
  );
};

export default PredictionForm;
