"""
Management command to seed the database with sample data.
Run with: python manage.py seed_data
"""

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from jobs.models import Category, Company, Job
from datetime import date, timedelta

User = get_user_model()


class Command(BaseCommand):
    help = 'Seeds the database with sample categories, companies, and jobs'

    def handle(self, *args, **options):
        self.stdout.write('Seeding database...\n')

        # ── Categories ──
        categories_data = [
            {'name': 'Engineering', 'slug': 'engineering', 'icon': '⚙️', 'description': 'Software & hardware engineering roles'},
            {'name': 'Design', 'slug': 'design', 'icon': '🎨', 'description': 'UI/UX, graphic, and product design'},
            {'name': 'Marketing', 'slug': 'marketing', 'icon': '📢', 'description': 'Digital marketing and growth roles'},
            {'name': 'Data Science', 'slug': 'data-science', 'icon': '📊', 'description': 'Analytics, ML, and data engineering'},
            {'name': 'Product', 'slug': 'product', 'icon': '🚀', 'description': 'Product management and strategy'},
            {'name': 'Finance', 'slug': 'finance', 'icon': '💰', 'description': 'Accounting, finance, and fintech'},
            {'name': 'Sales', 'slug': 'sales', 'icon': '🤝', 'description': 'Sales and business development'},
            {'name': 'Human Resources', 'slug': 'human-resources', 'icon': '👥', 'description': 'HR and people operations'},
        ]

        categories = {}
        for cat_data in categories_data:
            cat, created = Category.objects.get_or_create(
                slug=cat_data['slug'],
                defaults=cat_data,
            )
            categories[cat.slug] = cat
            status_text = 'Created' if created else 'Exists'
            self.stdout.write(f'  {status_text}: Category "{cat.name}"')

        # ── Companies ──
        companies_data = [
            {
                'name': 'TechNova Inc.',
                'website': 'https://technova.example.com',
                'description': 'Leading AI and cloud computing company building the future of enterprise software.',
                'location': 'San Francisco, CA',
                'industry': 'Technology',
                'employee_count': '1000-5000',
                'founded_year': 2015,
            },
            {
                'name': 'PixelCraft Studios',
                'website': 'https://pixelcraft.example.com',
                'description': 'Award-winning design agency creating beautiful digital experiences.',
                'location': 'New York, NY',
                'industry': 'Design Agency',
                'employee_count': '50-200',
                'founded_year': 2018,
            },
            {
                'name': 'DataFlow Analytics',
                'website': 'https://dataflow.example.com',
                'description': 'Big data analytics platform helping businesses make data-driven decisions.',
                'location': 'Austin, TX',
                'industry': 'Data Analytics',
                'employee_count': '200-500',
                'founded_year': 2016,
            },
            {
                'name': 'GreenScale Energy',
                'website': 'https://greenscale.example.com',
                'description': 'Renewable energy technology company powering a sustainable future.',
                'location': 'Denver, CO',
                'industry': 'Clean Energy',
                'employee_count': '500-1000',
                'founded_year': 2014,
            },
            {
                'name': 'CloudBridge Solutions',
                'website': 'https://cloudbridge.example.com',
                'description': 'Enterprise cloud infrastructure and DevOps consulting.',
                'location': 'Seattle, WA',
                'industry': 'Cloud Computing',
                'employee_count': '200-500',
                'founded_year': 2017,
            },
            {
                'name': 'FinWise Corp',
                'website': 'https://finwise.example.com',
                'description': 'Fintech startup revolutionizing personal finance and investing.',
                'location': 'Chicago, IL',
                'industry': 'Fintech',
                'employee_count': '100-200',
                'founded_year': 2019,
            },
            {
                'name': 'MediTech Health',
                'website': 'https://meditech.example.com',
                'description': 'Digital health platform connecting patients with modern healthcare.',
                'location': 'Boston, MA',
                'industry': 'Healthcare Tech',
                'employee_count': '500-1000',
                'founded_year': 2013,
            },
            {
                'name': 'Velocita Motors',
                'website': 'https://velocita.example.com',
                'description': 'Electric vehicle technology and autonomous driving systems.',
                'location': 'Detroit, MI',
                'industry': 'Automotive Tech',
                'employee_count': '1000-5000',
                'founded_year': 2016,
            },
        ]

        companies = {}
        for comp_data in companies_data:
            comp, created = Company.objects.get_or_create(
                name=comp_data['name'],
                defaults=comp_data,
            )
            companies[comp.name] = comp
            status_text = 'Created' if created else 'Exists'
            self.stdout.write(f'  {status_text}: Company "{comp.name}"')

        # ── Jobs ──
        jobs_data = [
            {
                'title': 'Senior Frontend Developer',
                'company': companies['TechNova Inc.'],
                'category': categories['engineering'],
                'description': 'We are looking for a talented Senior Frontend Developer to join our team and help build cutting-edge web applications. You will work with React, TypeScript, and modern CSS to create beautiful, performant user interfaces.',
                'requirements': 'At least 5 years of experience with JavaScript/TypeScript\nProficiency in React or Vue.js\nStrong CSS and responsive design skills\nExperience with REST APIs and GraphQL\nFamiliarity with CI/CD pipelines',
                'responsibilities': 'Build and maintain frontend applications\nCollaborate with designers and backend engineers\nMentor junior developers\nConduct code reviews\nOptimize application performance',
                'salary_min': 120000,
                'salary_max': 160000,
                'location': 'San Francisco, CA',
                'job_type': 'full-time',
                'experience_level': 'senior',
                'skills': 'React,TypeScript,CSS,GraphQL,Jest',
                'is_featured': True,
                'deadline': date.today() + timedelta(days=30),
            },
            {
                'title': 'UX/UI Designer',
                'company': companies['PixelCraft Studios'],
                'category': categories['design'],
                'description': 'Join our creative team to design beautiful, intuitive digital products. You will work closely with clients and developers to deliver exceptional user experiences from concept to implementation.',
                'requirements': 'Portfolio showcasing UX/UI design work\n3+ years experience in product design\nProficiency in Figma and Adobe Creative Suite\nStrong understanding of design systems\nExperience with user research and testing',
                'responsibilities': 'Create wireframes, prototypes, and high-fidelity mockups\nConduct user research and usability testing\nDevelop and maintain design systems\nCollaborate with development teams\nPresent design solutions to stakeholders',
                'salary_min': 90000,
                'salary_max': 130000,
                'location': 'New York, NY',
                'job_type': 'full-time',
                'experience_level': 'mid',
                'skills': 'Figma,Sketch,Adobe XD,User Research,Prototyping',
                'is_featured': True,
                'deadline': date.today() + timedelta(days=25),
            },
            {
                'title': 'Data Scientist',
                'company': companies['DataFlow Analytics'],
                'category': categories['data-science'],
                'description': 'We need a Data Scientist to analyze large datasets, build predictive models, and extract insights that drive business decisions. You will work with cutting-edge ML tools and big data platforms.',
                'requirements': 'Masters or PhD in Computer Science, Statistics, or related field\n3+ years experience in data science\nProficiency in Python, R, and SQL\nExperience with ML frameworks (TensorFlow, PyTorch, scikit-learn)\nStrong statistical analysis skills',
                'responsibilities': 'Develop and deploy ML models\nAnalyze large datasets for business insights\nCreate data visualizations and reports\nCollaborate with engineering to productionize models\nStay current with ML research',
                'salary_min': 130000,
                'salary_max': 175000,
                'location': 'Austin, TX',
                'job_type': 'full-time',
                'experience_level': 'senior',
                'skills': 'Python,TensorFlow,SQL,Pandas,Machine Learning',
                'is_featured': True,
                'deadline': date.today() + timedelta(days=20),
            },
            {
                'title': 'DevOps Engineer',
                'company': companies['CloudBridge Solutions'],
                'category': categories['engineering'],
                'description': 'Looking for a DevOps Engineer to design, implement, and manage our cloud infrastructure. You will build and optimize CI/CD pipelines and ensure high availability of our services.',
                'requirements': 'Strong experience with AWS or GCP\nProficiency in Docker and Kubernetes\nExperience with Terraform or CloudFormation\nKnowledge of Linux systems administration\nCI/CD pipeline experience (Jenkins, GitLab CI)',
                'responsibilities': 'Manage cloud infrastructure on AWS/GCP\nBuild and maintain CI/CD pipelines\nImplement monitoring and alerting\nAutomate deployment processes\nEnsure system security and compliance',
                'salary_min': 110000,
                'salary_max': 150000,
                'location': 'Seattle, WA',
                'job_type': 'remote',
                'experience_level': 'mid',
                'skills': 'AWS,Docker,Kubernetes,Terraform,Linux',
                'is_featured': False,
                'deadline': date.today() + timedelta(days=35),
            },
            {
                'title': 'Product Manager',
                'company': companies['TechNova Inc.'],
                'category': categories['product'],
                'description': 'We are seeking an experienced Product Manager to lead the development of our SaaS platform. You will define product strategy, work with cross-functional teams, and drive the product roadmap.',
                'requirements': '5+ years in product management\nExperience with agile methodologies\nStrong analytical and problem-solving skills\nExcellent communication and stakeholder management\nTechnical background preferred',
                'responsibilities': 'Define product vision and strategy\nManage the product backlog and roadmap\nConduct market research and competitive analysis\nWork closely with engineering and design teams\nAnalyze product metrics and user feedback',
                'salary_min': 135000,
                'salary_max': 180000,
                'location': 'San Francisco, CA',
                'job_type': 'full-time',
                'experience_level': 'senior',
                'skills': 'Product Strategy,Agile,Analytics,Stakeholder Management,Roadmapping',
                'is_featured': True,
                'deadline': date.today() + timedelta(days=28),
            },
            {
                'title': 'Digital Marketing Specialist',
                'company': companies['PixelCraft Studios'],
                'category': categories['marketing'],
                'description': 'Join our marketing team to develop and execute digital marketing strategies. You will manage campaigns across multiple channels and drive brand awareness and lead generation.',
                'requirements': '2+ years in digital marketing\nExperience with Google Ads, Facebook Ads\nKnowledge of SEO and content marketing\nFamiliarity with marketing analytics tools\nStrong copywriting skills',
                'responsibilities': 'Plan and execute digital marketing campaigns\nManage social media channels\nOptimize SEO and content strategy\nAnalyze campaign performance and ROI\nCollaborate with the design team on creative assets',
                'salary_min': 60000,
                'salary_max': 85000,
                'location': 'New York, NY',
                'job_type': 'full-time',
                'experience_level': 'entry',
                'skills': 'SEO,Google Ads,Social Media,Content Marketing,Analytics',
                'is_featured': False,
                'deadline': date.today() + timedelta(days=15),
            },
            {
                'title': 'Backend Developer (Python)',
                'company': companies['DataFlow Analytics'],
                'category': categories['engineering'],
                'description': 'We need a Backend Developer with strong Python skills to build scalable APIs and microservices. You will work on our core data platform processing millions of records daily.',
                'requirements': '3+ years of Python development\nExperience with Django or FastAPI\nStrong SQL and database design skills\nFamiliarity with message queues (RabbitMQ, Kafka)\nExperience with Docker and containerization',
                'responsibilities': 'Design and implement RESTful APIs\nOptimize database queries and data models\nBuild microservices architecture\nWrite unit and integration tests\nParticipate in architecture discussions',
                'salary_min': 100000,
                'salary_max': 140000,
                'location': 'Austin, TX',
                'job_type': 'remote',
                'experience_level': 'mid',
                'skills': 'Python,Django,PostgreSQL,Docker,Redis',
                'is_featured': False,
                'deadline': date.today() + timedelta(days=22),
            },
            {
                'title': 'Financial Analyst',
                'company': companies['FinWise Corp'],
                'category': categories['finance'],
                'description': 'Seeking a Financial Analyst to support our fintech products with data-driven financial analysis, forecasting, and modeling.',
                'requirements': 'Bachelors in Finance, Economics, or related field\n2+ years of financial analysis experience\nProficiency in Excel and financial modeling\nKnowledge of fintech industry\nCFA or CPA preferred',
                'responsibilities': 'Build financial models and forecasts\nAnalyze business performance metrics\nPrepare reports for stakeholders\nSupport product pricing decisions\nConduct market and competitor analysis',
                'salary_min': 75000,
                'salary_max': 100000,
                'location': 'Chicago, IL',
                'job_type': 'full-time',
                'experience_level': 'entry',
                'skills': 'Financial Modeling,Excel,SQL,Forecasting,Analysis',
                'is_featured': False,
                'deadline': date.today() + timedelta(days=18),
            },
            {
                'title': 'Machine Learning Engineer',
                'company': companies['MediTech Health'],
                'category': categories['data-science'],
                'description': 'Build ML models that improve healthcare outcomes. Work on natural language processing, computer vision, and predictive analytics in our health platform.',
                'requirements': 'Masters in CS, ML, or related field\nExperience deploying ML models to production\nProficiency in Python and ML frameworks\nExperience with NLP or computer vision\nKnowledge of healthcare data (HIPAA) preferred',
                'responsibilities': 'Develop and deploy ML models for health predictions\nProcess and analyze medical datasets\nBuild data pipelines for model training\nCollaborate with medical professionals\nMonitor model performance in production',
                'salary_min': 140000,
                'salary_max': 190000,
                'location': 'Boston, MA',
                'job_type': 'full-time',
                'experience_level': 'senior',
                'skills': 'Python,PyTorch,NLP,Computer Vision,MLOps',
                'is_featured': True,
                'deadline': date.today() + timedelta(days=40),
            },
            {
                'title': 'Sales Development Representative',
                'company': companies['CloudBridge Solutions'],
                'category': categories['sales'],
                'description': 'Join our sales team to generate new business opportunities. You will prospect, qualify leads, and schedule demos for our enterprise cloud solutions.',
                'requirements': '1+ years in B2B sales or SDR role\nExcellent communication skills\nExperience with CRM tools (Salesforce, HubSpot)\nSelf-motivated and goal-oriented\nTech industry experience preferred',
                'responsibilities': 'Prospect and qualify new leads\nConduct outreach via email and phone\nSchedule product demos for account executives\nMaintain CRM records\nMeet monthly activity and pipeline targets',
                'salary_min': 55000,
                'salary_max': 75000,
                'location': 'Seattle, WA',
                'job_type': 'full-time',
                'experience_level': 'entry',
                'skills': 'Sales,CRM,Communication,Lead Generation,B2B',
                'is_featured': False,
                'deadline': date.today() + timedelta(days=12),
            },
            {
                'title': 'Embedded Systems Engineer',
                'company': companies['Velocita Motors'],
                'category': categories['engineering'],
                'description': 'Design and develop embedded software for our next-generation electric vehicle systems. Work on real-time operating systems, sensor integration, and vehicle control modules.',
                'requirements': 'BS/MS in Electrical or Computer Engineering\n4+ years embedded systems experience\nProficiency in C/C++ for embedded platforms\nExperience with RTOS (FreeRTOS, QNX)\nKnowledge of automotive protocols (CAN, LIN)',
                'responsibilities': 'Develop embedded firmware for vehicle systems\nIntegrate sensors and actuators\nOptimize real-time performance\nWrite hardware abstraction layers\nConduct testing and debugging on hardware',
                'salary_min': 115000,
                'salary_max': 155000,
                'location': 'Detroit, MI',
                'job_type': 'full-time',
                'experience_level': 'mid',
                'skills': 'C,C++,RTOS,Embedded Systems,CAN Bus',
                'is_featured': False,
                'deadline': date.today() + timedelta(days=30),
            },
            {
                'title': 'HR Business Partner',
                'company': companies['GreenScale Energy'],
                'category': categories['human-resources'],
                'description': 'Partner with leadership to develop and implement HR strategies that support business objectives. Focus on talent management, culture, and employee engagement.',
                'requirements': '5+ years in HR or people operations\nExperience as an HR business partner\nKnowledge of employment law and compliance\nStrong interpersonal and coaching skills\nPHR or SHRM-CP certification preferred',
                'responsibilities': 'Advise leadership on HR strategy\nManage employee relations and performance\nDrive talent acquisition and retention\nDevelop training and development programs\nEnsure HR compliance and best practices',
                'salary_min': 85000,
                'salary_max': 115000,
                'location': 'Denver, CO',
                'job_type': 'full-time',
                'experience_level': 'senior',
                'skills': 'HR Strategy,Talent Management,Employee Relations,Compliance,Coaching',
                'is_featured': False,
                'deadline': date.today() + timedelta(days=25),
            },
            {
                'title': 'React Native Developer',
                'company': companies['FinWise Corp'],
                'category': categories['engineering'],
                'description': 'Build our mobile banking app using React Native. Create smooth, performant mobile experiences for iOS and Android that handle financial transactions securely.',
                'requirements': '3+ years React Native development\nExperience publishing apps to App Store and Play Store\nStrong JavaScript/TypeScript skills\nKnowledge of mobile security best practices\nExperience with state management (Redux, MobX)',
                'responsibilities': 'Develop cross-platform mobile features\nOptimize app performance and startup time\nImplement secure payment flows\nWrite automated tests\nCollaborate with backend and design teams',
                'salary_min': 105000,
                'salary_max': 145000,
                'location': 'Chicago, IL',
                'job_type': 'remote',
                'experience_level': 'mid',
                'skills': 'React Native,TypeScript,Redux,Mobile Development,Jest',
                'is_featured': True,
                'deadline': date.today() + timedelta(days=28),
            },
            {
                'title': 'Content Marketing Manager',
                'company': companies['MediTech Health'],
                'category': categories['marketing'],
                'description': 'Lead our content marketing strategy to establish thought leadership in digital health. Create compelling content that educates and engages healthcare professionals and patients.',
                'requirements': '4+ years in content marketing\nExperience in healthcare or B2B tech\nStrong writing and editing skills\nKnowledge of SEO and content analytics\nExperience managing a content calendar',
                'responsibilities': 'Develop content strategy and editorial calendar\nCreate blog posts, whitepapers, and case studies\nManage content team and freelance writers\nOptimize content for SEO and conversions\nMeasure content performance and ROI',
                'salary_min': 80000,
                'salary_max': 110000,
                'location': 'Boston, MA',
                'job_type': 'full-time',
                'experience_level': 'mid',
                'skills': 'Content Strategy,SEO,Copywriting,Analytics,Healthcare',
                'is_featured': False,
                'deadline': date.today() + timedelta(days=20),
            },
            {
                'title': 'Sustainability Engineer',
                'company': companies['GreenScale Energy'],
                'category': categories['engineering'],
                'description': 'Drive the development of renewable energy solutions. Work on solar, wind, and battery storage technologies to help build a sustainable future.',
                'requirements': 'BS/MS in Environmental or Mechanical Engineering\n3+ years in renewable energy\nKnowledge of energy systems and grid integration\nExperience with simulation tools\nFamiliarity with regulatory frameworks',
                'responsibilities': 'Design renewable energy systems\nConduct feasibility studies and simulations\nOptimize energy storage solutions\nCollaborate with project teams\nEnsure compliance with environmental regulations',
                'salary_min': 95000,
                'salary_max': 130000,
                'location': 'Denver, CO',
                'job_type': 'full-time',
                'experience_level': 'mid',
                'skills': 'Renewable Energy,Solar,Wind,Energy Storage,Simulation',
                'is_featured': False,
                'deadline': date.today() + timedelta(days=35),
            },
            {
                'title': 'QA Automation Engineer',
                'company': companies['TechNova Inc.'],
                'category': categories['engineering'],
                'description': 'Build and maintain our automated testing infrastructure. Ensure the quality and reliability of our software products through comprehensive test coverage.',
                'requirements': '3+ years in QA automation\nProficiency in Selenium, Cypress, or Playwright\nExperience with CI/CD integration\nStrong Python or JavaScript skills\nKnowledge of API testing tools',
                'responsibilities': 'Design and implement automated test suites\nIntegrate tests into CI/CD pipelines\nPerform exploratory and regression testing\nTrack and report quality metrics\nCollaborate with developers on testability',
                'salary_min': 90000,
                'salary_max': 125000,
                'location': 'San Francisco, CA',
                'job_type': 'remote',
                'experience_level': 'mid',
                'skills': 'Selenium,Cypress,Python,CI/CD,API Testing',
                'is_featured': False,
                'deadline': date.today() + timedelta(days=22),
            },
        ]

        for job_data in jobs_data:
            job, created = Job.objects.get_or_create(
                title=job_data['title'],
                company=job_data['company'],
                defaults=job_data,
            )
            status_text = 'Created' if created else 'Exists'
            self.stdout.write(f'  {status_text}: Job "{job.title}"')

        # ── Create demo user ──
        if not User.objects.filter(email='demo@careernest.com').exists():
            User.objects.create_user(
                email='demo@careernest.com',
                password='demo1234',
                full_name='Alex Johnson',
                job_title='Full Stack Developer',
                location='San Francisco, CA',
                bio='Passionate developer looking for new opportunities.',
            )
            self.stdout.write('  Created: Demo user (demo@careernest.com / demo1234)')

        # ── Create admin user ──
        if not User.objects.filter(email='admin@careernest.com').exists():
            User.objects.create_superuser(
                email='admin@careernest.com',
                password='admin1234',
                full_name='Admin User',
            )
            self.stdout.write('  Created: Admin user (admin@careernest.com / admin1234)')

        self.stdout.write(self.style.SUCCESS('\n[OK] Database seeded successfully!'))
