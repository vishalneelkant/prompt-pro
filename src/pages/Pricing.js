import React, { useState } from 'react';
import SEO from '../components/SEO';
import StructuredData, { pricingPageSchema } from '../components/StructuredData';
import './Pricing.css';

const Pricing = () => {
  const [billingCycle, setBillingCycle] = useState('monthly');

  const plans = [
    {
      name: 'Free',
      price: { monthly: 0, yearly: 0 },
      description: 'Perfect for getting started with prompt optimization',
      features: [
        '10 prompt optimizations per day',
        'Basic optimization strategies',
        'Standard response time',
        'Community support',
        'Basic grammar correction'
      ],
      popular: false,
      cta: 'Get Started Free'
    },
    {
      name: 'Pro',
      price: { monthly: 5, yearly: 60 },
      description: 'Ideal for professionals and content creators',
      features: [
        'Unlimited prompt optimizations',
        'Advanced optimization strategies',
        'Priority response time',
        'Email support',
        'Advanced grammar & style correction',
        'Save to personal library',
        'Export optimized prompts',
        'Custom context options'
      ],
      popular: true,
      cta: 'Start Pro Trial'
    },
    {
      name: 'Enterprise',
      price: { monthly: 9, yearly: 99 },
      description: 'Built for teams and organizations',
      features: [
        'Everything in Pro',
        'Team collaboration tools',
        'Shared prompt libraries',
        'Advanced analytics',
        'Priority support',
        'Custom integrations',
        'SSO authentication',
        'Dedicated account manager',
        'Custom training sessions'
      ],
      popular: false,
      cta: 'Contact Sales'
    }
  ];

  const getPrice = (plan) => {
    const price = plan.price[billingCycle];
    return price === 0 ? 'Free' : `$${price}`;
  };

  const getSavings = (plan) => {
    if (billingCycle === 'yearly' && plan.price.monthly > 0) {
      const monthlyCost = plan.price.monthly * 12;
      const savings = monthlyCost - plan.price.yearly;
      return Math.round((savings / monthlyCost) * 100);
    }
    return 0;
  };

  return (
    <>
      <SEO 
        title="Pricing Plans - Affordable AI Prompt Optimization"
        description="Choose the perfect PromptVita plan for your needs. Free plan available! Pro at $5/month, Enterprise at $9/month. AI-powered prompt optimization for everyone."
        keywords="promptvita pricing, prompt optimization pricing, AI writing tool cost, prompt engineering plans, affordable AI tools, prompt optimizer subscription"
        canonical="https://www.promptvita.com/pricing"
      />
      <StructuredData data={pricingPageSchema} />
      <div className="pricing">
      <div className="pricing-container">
        <div className="pricing-hero">
          <h1>Simple, Transparent Pricing</h1>
          <p className="pricing-subtitle">
            Choose the perfect plan for your prompt optimization needs. 
            All plans include our core optimization features.
          </p>
          
          <div className="billing-toggle">
            <button 
              className={billingCycle === 'monthly' ? 'active' : ''}
              onClick={() => setBillingCycle('monthly')}
            >
              Monthly
            </button>
            <button 
              className={billingCycle === 'yearly' ? 'active' : ''}
              onClick={() => setBillingCycle('yearly')}
            >
              Yearly
              <span className="savings-badge">Save 20%</span>
            </button>
          </div>
        </div>

        <div className="pricing-grid">
          {plans.map((plan, index) => (
            <div key={index} className={`pricing-card ${plan.popular ? 'popular' : ''}`}>
              {plan.popular && <div className="popular-badge">Most Popular</div>}
              
              <div className="plan-header">
                <h3 className="plan-name">{plan.name}</h3>
                <div className="plan-price">
                  <span className="price">{getPrice(plan)}</span>
                  {plan.price[billingCycle] > 0 && (
                    <span className="price-period">
                      /{billingCycle === 'monthly' ? 'month' : 'year'}
                    </span>
                  )}
                </div>
                {getSavings(plan) > 0 && (
                  <div className="savings">Save {getSavings(plan)}%</div>
                )}
                <p className="plan-description">{plan.description}</p>
              </div>

              <div className="plan-features">
                <ul>
                  {plan.features.map((feature, featureIndex) => (
                    <li key={featureIndex}>
                      <span className="feature-icon">✓</span>
                      {feature}
                    </li>
                  ))}
                </ul>
              </div>

              <button className={`plan-cta ${plan.popular ? 'primary' : 'secondary'}`}>
                {plan.cta}
              </button>
            </div>
          ))}
        </div>

        {/* Trust / Guarantee Strip */}
        <div className="trust-strip" role="note" aria-label="Trust and guarantee">
          <div className="trust-item">✅ 7‑day money‑back guarantee</div>
          <div className="trust-dot">•</div>
          <div className="trust-item">🔒 Secure payments</div>
          <div className="trust-dot">•</div>
          <div className="trust-item">📞 Priority support on Pro & Enterprise</div>
        </div>

        {/* Compact Feature Comparison */}
        <div className="comparison">
          <h3>Compare features</h3>
          <div className="comparison-table" role="table" aria-label="Pricing comparison">
            <div className="row header" role="row">
              <div className="cell" role="columnheader">Feature</div>
              <div className="cell" role="columnheader">Free</div>
              <div className="cell" role="columnheader">Pro</div>
              <div className="cell" role="columnheader">Enterprise</div>
            </div>
            {[
              ['Daily optimizations', '10', 'Unlimited', 'Unlimited'],
              ['Optimization strategies', 'Basic', 'Advanced', 'Advanced + Custom'],
              ['Response speed', 'Standard', 'Priority', 'Priority'],
              ['Team collaboration', '—', '—', '✓'],
              ['Shared libraries', '—', '✓', '✓']
            ].map((r, i) => (
              <div className="row" role="row" key={i}>
                <div className="cell label" role="cell">{r[0]}</div>
                <div className="cell" role="cell">{r[1]}</div>
                <div className="cell" role="cell">{r[2]}</div>
                <div className="cell" role="cell">{r[3]}</div>
              </div>
            ))}
          </div>
        </div>

        <div className="pricing-faq">
          <h2>Frequently Asked Questions</h2>
          <div className="faq-grid" role="region" aria-label="FAQs">
            {[
              ['What counts as a prompt optimization?', 'Each time you submit a prompt for optimization, it counts as one optimization. This includes both text correction and prompt enhancement.'],
              ['Can I change plans anytime?', 'Yes, you can upgrade or downgrade your plan at any time. Changes will be reflected in your next billing cycle.'],
              ['Is there a free trial for Pro?', 'Yes, we offer a 7-day free trial for the Pro plan. No credit card required to start your trial.'],
              ['What payment methods do you accept?', 'We accept all major credit cards, PayPal, and bank transfers for Enterprise plans.']
            ].map((faq, idx) => (
              <details key={idx} className="faq-item">
                <summary aria-expanded="false"><h4>{faq[0]}</h4></summary>
                <p>{faq[1]}</p>
              </details>
            ))}
          </div>
        </div>

        <div className="pricing-cta">
          <h2>Ready to Get Started?</h2>
          <p>Join thousands of users who are already optimizing their prompts with PromptVita.</p>
          <div className="cta-buttons">
            <a href="/" className="cta-button primary">Start Free Trial</a>
            <button className="cta-button secondary" onClick={() => alert('Contact sales functionality not implemented yet')}>Contact Sales</button>
          </div>
        </div>
      </div>
    </div>
    </>
  );
};

export default Pricing;
