import React, { useState } from 'react';

function App() {
    const [activeTab, setActiveTab] = useState('text');
    const [inputVal, setInputVal] = useState('');
    const [file, setFile] = useState(null);
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState(null);
    const [error, setError] = useState(null);

    const handleProcess = async () => {
        setLoading(true);
        setError(null);
        setResult(null);

        const formData = new FormData();
        let url = "http://127.0.0.1:8000/process/";

        if (activeTab === 'text') {
            url += "text";
            formData.append("text", inputVal);
        } else if (activeTab === 'news') {
            url += "news";
            formData.append("url", inputVal);
        } else if (activeTab === 'image' || activeTab === 'voice') {
            url += activeTab;
            if (file) {
                formData.append("file", file);
            } else {
                setError("Please select a file.");
                setLoading(false);
                return;
            }
        }

        try {
            const resp = await fetch(url, {
                method: 'POST',
                body: formData,
            });
            if (resp.ok) {
                const data = await resp.json();
                setResult(data);
            } else {
                setError("Failed to fetch from backend. Error " + resp.status);
            }
        } catch (err) {
            setError("Network or Server error: " + err.message);
        }
        setLoading(false);
    };

    return (
        <div style={{ padding: '40px', maxWidth: '900px', margin: '0 auto', fontFamily: 'Inter, sans-serif' }}>
            <h1 style={{ textAlign: 'center', color: '#111827', fontSize: '2.5rem' }}>🌐 Universal AI Bridge</h1>
            <p style={{ textAlign: 'center', color: '#4B5563', fontSize: '1.2rem', marginBottom: '40px' }}>
                Instantly convert messy, chaotic inputs into structured, life-saving actions using Gemini AI.
            </p>

            {/* Tabs */}
            <div style={{ display: 'flex', gap: '10px', marginBottom: '20px', justifyContent: 'center' }}>
                {['text', 'image', 'voice', 'news'].map((tab) => (
                    <button
                        key={tab}
                        onClick={() => { setActiveTab(tab); setResult(null); setError(null); setFile(null); setInputVal(''); }}
                        style={{
                            padding: '12px 24px',
                            borderRadius: '8px',
                            border: 'none',
                            cursor: 'pointer',
                            fontWeight: '600',
                            backgroundColor: activeTab === tab ? '#3B82F6' : '#E5E7EB',
                            color: activeTab === tab ? 'white' : '#374151',
                            transition: 'all 0.2s',
                        }}
                    >
                        {tab.charAt(0).toUpperCase() + tab.slice(1)}
                    </button>
                ))}
            </div>

            {/* Input Section */}
            <div style={{ backgroundColor: '#F9FAFB', padding: '30px', borderRadius: '12px', border: '1px solid #E5E7EB', boxShadow: '0 4px 6px -1px rgba(0,0,0,0.1)' }}>
                {activeTab === 'text' && (
                    <textarea
                        rows="5"
                        placeholder="E.g., My father has chest pain near Whitefield. What should I do?"
                        value={inputVal}
                        onChange={(e) => setInputVal(e.target.value)}
                        style={{ width: '100%', padding: '15px', borderRadius: '8px', border: '1px solid #D1D5DB', fontSize: '1rem', boxSizing: 'border-box' }}
                    />
                )}
                {activeTab === 'news' && (
                    <input
                        type="url"
                        placeholder="Enter Breaking News URL..."
                        value={inputVal}
                        onChange={(e) => setInputVal(e.target.value)}
                        style={{ width: '100%', padding: '15px', borderRadius: '8px', border: '1px solid #D1D5DB', fontSize: '1rem', boxSizing: 'border-box' }}
                    />
                )}
                {(activeTab === 'image' || activeTab === 'voice') && (
                    <input
                        type="file"
                        onChange={(e) => setFile(e.target.files[0])}
                        style={{ width: '100%', padding: '15px', borderRadius: '8px', border: '2px dashed #D1D5DB', backgroundColor: 'white', boxSizing: 'border-box' }}
                    />
                )}

                <button
                    onClick={handleProcess}
                    disabled={loading}
                    style={{
                        marginTop: '20px',
                        width: '100%',
                        padding: '16px',
                        borderRadius: '8px',
                        border: 'none',
                        backgroundColor: loading ? '#9CA3AF' : '#10B981',
                        color: 'white',
                        fontWeight: 'bold',
                        fontSize: '1.1rem',
                        cursor: loading ? 'not-allowed' : 'pointer',
                        boxShadow: '0 4px 6px -1px rgba(16, 185, 129, 0.4)',
                        transition: 'background-color 0.2s',
                    }}
                >
                    {loading ? "Processing via Gemini Agent..." : "Analyze & Act"}
                </button>
            </div>

            {error && (
                <div style={{ marginTop: '20px', padding: '15px', backgroundColor: '#FEE2E2', color: '#DC2626', borderRadius: '8px', fontWeight: '500' }}>
                    ❌ {error}
                </div>
            )}

            {/* Results Section */}
            {result && (
                <div style={{ marginTop: '30px', animation: 'fadeIn 0.5s ease-in' }}>
                    <h2 style={{ color: '#1F2937', marginBottom: '20px', textAlign: 'center' }}>🧠 Agent Analysis Report</h2>

                    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: '20px', marginBottom: '20px' }}>
                        <div style={{ backgroundColor: '#F3F4F6', padding: '20px', borderRadius: '12px', textAlign: 'center' }}>
                            <h4 style={{ margin: 0, color: '#6B7280' }}>Intent</h4>
                            <p style={{ margin: '10px 0 0', fontWeight: 'bold', fontSize: '1.2rem', color: '#111827' }}>{result.intent || 'Unknown'}</p>
                        </div>
                        <div style={{ backgroundColor: '#F3F4F6', padding: '20px', borderRadius: '12px', textAlign: 'center' }}>
                            <h4 style={{ margin: 0, color: '#6B7280' }}>Category</h4>
                            <p style={{ margin: '10px 0 0', fontWeight: 'bold', fontSize: '1.2rem', color: '#111827' }}>{result.category?.toUpperCase() || 'GENERAL'}</p>
                        </div>
                        <div style={{ backgroundColor: result.urgency === 'CRITICAL' || result.urgency === 'HIGH' ? '#FEF2F2' : '#ECFDF5', padding: '20px', borderRadius: '12px', textAlign: 'center', border: result.urgency === 'CRITICAL' ? '2px solid #EF4444' : 'none' }}>
                            <h4 style={{ margin: 0, color: result.urgency === 'CRITICAL' ? '#DC2626' : '#059669' }}>Urgency</h4>
                            <p style={{ margin: '10px 0 0', fontWeight: '900', fontSize: '1.4rem', color: result.urgency === 'CRITICAL' || result.urgency === 'HIGH' ? '#DC2626' : '#059669' }}>
                                {result.urgency || 'LOW'}
                            </p>
                        </div>
                    </div>

                    <div style={{ backgroundColor: 'white', border: '1px solid #E5E7EB', padding: '25px', borderRadius: '12px', marginBottom: '20px' }}>
                        <h3 style={{ marginTop: 0, color: '#374151' }}>📋 Situation Summary</h3>
                        <p style={{ fontSize: '1.1rem', color: '#1F2937', lineHeight: '1.6' }}>{result.summary}</p>
                    </div>

                    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px' }}>
                        <div style={{ backgroundColor: '#F0FDF4', border: '1px solid #BBF7D0', padding: '25px', borderRadius: '12px' }}>
                            <h3 style={{ marginTop: 0, color: '#166534', display: 'flex', alignItems: 'center', gap: '8px' }}>✅ Required Actions</h3>
                            <ul style={{ paddingLeft: '20px', color: '#14532D', margin: 0 }}>
                                {result.actions?.map((act, i) => (
                                    <li key={i} style={{ marginBottom: '10px', fontSize: '1.05rem' }}>{act}</li>
                                ))}
                            </ul>
                        </div>

                        <div style={{ backgroundColor: '#FFFBEB', border: '1px solid #FDE68A', padding: '25px', borderRadius: '12px' }}>
                            <h3 style={{ marginTop: 0, color: '#92400E', display: 'flex', alignItems: 'center', gap: '8px' }}>🔄 Next Steps</h3>
                            <ul style={{ paddingLeft: '20px', color: '#78350F', margin: 0 }}>
                                {result.next_steps?.map((step, i) => (
                                    <li key={i} style={{ marginBottom: '10px', fontSize: '1.05rem' }}>{step}</li>
                                ))}
                            </ul>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
}

export default App;