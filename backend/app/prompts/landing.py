LANDING_PROMPT = """You are a frontend developer and conversion optimization expert. Create a complete, responsive HTML landing page for the product: "{idea}".

Product name: {product_name}
Description: {description}
Features: {features}

Requirements:
- Use Tailwind CSS via CDN
- Include hero section with headline, subheadline, and CTA button
- Features section with icons
- Pricing section (3 tiers)
- Testimonials section
- FAQ section
- Email capture form (footer)
- Responsive design
- Modern, clean aesthetic
- Dark mode support

Output ONLY the complete HTML file content, wrapped in triple backticks. No explanations."""