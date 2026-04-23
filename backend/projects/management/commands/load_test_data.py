import random
from datetime import date, timedelta
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from projects.models import Client, Project, Phase, Task, Milestone, ProjectNote
from resources.models import EquipmentCategory, Equipment, MaterialCategory, Material, ResourceAllocation, MaintenanceRecord
from finance.models import Budget, BudgetCategory, BudgetItem, Invoice, Payment, Expense
from procurement.models import Vendor, PurchaseOrder, PurchaseOrderItem, InventoryTransaction
from hr.models import Department, JobTitle, Employee, Attendance, LeaveType, LeaveRequest, Payroll
from documents.models import DocumentCategory, Document


def d(days_offset):
    return date.today() + timedelta(days=days_offset)


class Command(BaseCommand):
    help = 'Load comprehensive test data for all ERP modules'

    def handle(self, *args, **kwargs):
        self.stdout.write('Loading test data...')

        # ── Users ──────────────────────────────────────────────
        admin, _ = User.objects.get_or_create(username='admin', defaults={'is_superuser': True, 'is_staff': True, 'email': 'admin@erp.com'})
        admin.set_password('admin123')
        admin.save()

        pm1, _ = User.objects.get_or_create(username='pm_khalid', defaults={'first_name': 'Khalid', 'last_name': 'Al Rashid', 'email': 'khalid@erp.com', 'is_staff': True})
        pm1.set_password('pass1234')
        pm1.save()

        pm2, _ = User.objects.get_or_create(username='pm_sarah', defaults={'first_name': 'Sarah', 'last_name': 'Mohammed', 'email': 'sarah@erp.com', 'is_staff': True})
        pm2.set_password('pass1234')
        pm2.save()

        # ── Clients ────────────────────────────────────────────
        c1, _ = Client.objects.get_or_create(name='Abu Dhabi Municipality', defaults={'contact_person': 'Ahmed Al Mansouri', 'email': 'ahmed@adm.ae', 'phone': '+971-2-555-0100', 'address': 'Abu Dhabi, UAE'})
        c2, _ = Client.objects.get_or_create(name='Emaar Properties', defaults={'contact_person': 'Sara Al Hashimi', 'email': 'sara@emaar.ae', 'phone': '+971-4-555-0200', 'address': 'Dubai, UAE'})
        c3, _ = Client.objects.get_or_create(name='Kuwait Municipality', defaults={'contact_person': 'Fahad Al Sabah', 'email': 'fahad@km.kw', 'phone': '+965-555-0300', 'address': 'Kuwait City, Kuwait'})

        # ── Projects ───────────────────────────────────────────
        projects_data = [
            dict(name='Marina Tower Complex', code='PRJ-001', client=c1, project_manager=pm1,
                 location='Abu Dhabi Corniche', start_date=d(-180), end_date=d(365),
                 status='active', priority='high', budget=45000000, completion_percentage=38),
            dict(name='Downtown Bridge Expansion', code='PRJ-002', client=c2, project_manager=pm2,
                 location='Dubai Downtown', start_date=d(-90), end_date=d(275),
                 status='active', priority='critical', budget=12500000, completion_percentage=61),
            dict(name='Al Ain Road Rehabilitation', code='PRJ-003', client=c1, project_manager=pm1,
                 location='Al Ain City', start_date=d(30), end_date=d(300),
                 status='planning', priority='medium', budget=3200000, completion_percentage=0),
            dict(name='Kuwait Waterfront Development', code='PRJ-004', client=c3, project_manager=pm2,
                 location='Kuwait City Seafront', start_date=d(-365), end_date=d(-30),
                 status='completed', priority='high', budget=28000000, completion_percentage=100),
            dict(name='Yas Island Infrastructure', code='PRJ-005', client=c2, project_manager=pm1,
                 location='Yas Island, Abu Dhabi', start_date=d(-30), end_date=d(500),
                 status='active', priority='high', budget=67000000, completion_percentage=12),
        ]
        projects = []
        for pd in projects_data:
            p, _ = Project.objects.get_or_create(code=pd['code'], defaults=pd)
            projects.append(p)

        p1, p2, p3, p4, p5 = projects

        # ── Phases & Tasks ─────────────────────────────────────
        phases_data = [
            (p1, 'Site Preparation & Excavation', 1, d(-180), d(-60), 'completed', 100),
            (p1, 'Foundation & Piling Works', 2, d(-60), d(60), 'completed', 100),
            (p1, 'Structural Steel & Concrete', 3, d(60), d(200), 'in_progress', 30),
            (p1, 'MEP Works', 4, d(200), d(320), 'pending', 0),
            (p1, 'Finishing & Handover', 5, d(320), d(365), 'pending', 0),
            (p2, 'Survey & Design', 1, d(-90), d(-45), 'completed', 100),
            (p2, 'Demolition & Groundwork', 2, d(-45), d(30), 'completed', 100),
            (p2, 'Bridge Deck Construction', 3, d(30), d(180), 'in_progress', 55),
            (p2, 'Road Works & Connections', 4, d(180), d(275), 'pending', 0),
            (p5, 'Master Planning', 1, d(-30), d(30), 'in_progress', 70),
            (p5, 'Utilities & Services', 2, d(30), d(200), 'pending', 0),
            (p5, 'Roads & Landscaping', 3, d(200), d(400), 'pending', 0),
        ]
        phases = []
        for ph_d in phases_data:
            ph, _ = Phase.objects.get_or_create(
                project=ph_d[0], name=ph_d[1],
                defaults=dict(sequence=ph_d[2], start_date=ph_d[3], end_date=ph_d[4], status=ph_d[5], completion_percentage=ph_d[6], budget=ph_d[0].budget / 5)
            )
            phases.append(ph)

        task_statuses = ['completed', 'completed', 'in_progress', 'todo', 'blocked']
        for ph in phases[:6]:
            for i, task_name in enumerate(['Site survey', 'Engineering drawings', 'Material procurement', 'Construction works', 'Quality inspection']):
                Task.objects.get_or_create(
                    phase=ph, name=task_name,
                    defaults=dict(status=task_statuses[i], priority='medium', estimated_hours=80, completion_percentage=100 if task_statuses[i] == 'completed' else 50 if task_statuses[i] == 'in_progress' else 0)
                )

        # ── Milestones ─────────────────────────────────────────
        milestones_data = [
            (p1, 'Excavation Complete', d(-60), 'achieved'),
            (p1, 'Foundation Complete', d(60), 'achieved'),
            (p1, 'Structure Topping Out', d(200), 'upcoming'),
            (p1, 'Practical Completion', d(360), 'upcoming'),
            (p2, 'Design Approval', d(-80), 'achieved'),
            (p2, 'Deck Launch', d(50), 'achieved'),
            (p2, 'Bridge Opening', d(270), 'at_risk'),
            (p4, 'Final Handover', d(-30), 'achieved'),
            (p5, 'Planning Approval', d(30), 'upcoming'),
        ]
        for m_d in milestones_data:
            Milestone.objects.get_or_create(project=m_d[0], name=m_d[1], defaults=dict(date=m_d[2], status=m_d[3]))

        # ── Departments & Job Titles ───────────────────────────
        depts = {}
        for code, name in [('ENG', 'Engineering'), ('PM', 'Project Management'), ('HR', 'Human Resources'), ('FIN', 'Finance'), ('PROC', 'Procurement'), ('HSE', 'Health, Safety & Environment')]:
            dept, _ = Department.objects.get_or_create(code=code, defaults={'name': name})
            depts[code] = dept

        titles = {}
        title_data = [
            ('Senior Engineer', 'ENG'), ('Civil Engineer', 'ENG'), ('Structural Engineer', 'ENG'),
            ('Project Manager', 'PM'), ('Site Engineer', 'PM'), ('Planning Engineer', 'PM'),
            ('HR Manager', 'HR'), ('Recruiter', 'HR'),
            ('Finance Manager', 'FIN'), ('Accountant', 'FIN'),
            ('Procurement Manager', 'PROC'), ('Buyer', 'PROC'),
            ('HSE Manager', 'HSE'), ('Safety Officer', 'HSE'),
        ]
        for title_name, dept_code in title_data:
            t, _ = JobTitle.objects.get_or_create(name=title_name, defaults={'department': depts[dept_code]})
            titles[title_name] = t

        # ── Employees ──────────────────────────────────────────
        employees_data = [
            ('EMP-001', 'Khalid', 'Al Mansouri', 'ENG', 'Senior Engineer', 18000, d(-1500)),
            ('EMP-002', 'Sarah', 'Mohammed', 'PM', 'Project Manager', 22000, d(-900)),
            ('EMP-003', 'John', 'Williams', 'ENG', 'Civil Engineer', 14000, d(-600)),
            ('EMP-004', 'Fatima', 'Al Zaabi', 'HR', 'HR Manager', 12000, d(-1200)),
            ('EMP-005', 'Mohammed', 'Hassan', 'FIN', 'Finance Manager', 16000, d(-800)),
            ('EMP-006', 'Priya', 'Kumar', 'FIN', 'Accountant', 9000, d(-400)),
            ('EMP-007', 'Ahmed', 'Al Rashid', 'PROC', 'Procurement Manager', 14000, d(-700)),
            ('EMP-008', 'Linda', 'Santos', 'ENG', 'Structural Engineer', 13000, d(-300)),
            ('EMP-009', 'Omar', 'Al Farsi', 'HSE', 'HSE Manager', 13500, d(-500)),
            ('EMP-010', 'Yusuf', 'Ibrahim', 'PM', 'Planning Engineer', 11000, d(-200)),
            ('EMP-011', 'Nora', 'Al Suwaidi', 'HR', 'Recruiter', 7500, d(-150)),
            ('EMP-012', 'David', 'Chen', 'ENG', 'Site Engineer', 10000, d(-100)),
        ]
        employees = []
        for emp_d in employees_data:
            emp, _ = Employee.objects.get_or_create(employee_id=emp_d[0], defaults=dict(
                first_name=emp_d[1], last_name=emp_d[2],
                email=f"{emp_d[0].lower()}@erp.com",
                department=depts[emp_d[3]], job_title=titles[emp_d[4]],
                base_salary=emp_d[5], hire_date=emp_d[6],
                status='active', employment_type='full_time'
            ))
            employees.append(emp)

        # ── Attendance (last 5 days) ───────────────────────────
        statuses = ['present', 'present', 'present', 'present', 'half_day']
        for emp in employees[:8]:
            for i in range(5):
                att_date = d(-i)
                Attendance.objects.get_or_create(employee=emp, date=att_date, defaults=dict(
                    check_in=None if i == 0 else None,
                    status=statuses[i % len(statuses)],
                    overtime_hours=1.5 if i % 3 == 0 else 0
                ))

        # ── Leave Types & Requests ─────────────────────────────
        annual, _ = LeaveType.objects.get_or_create(name='Annual Leave', defaults={'days_allowed': 30, 'is_paid': True})
        sick, _ = LeaveType.objects.get_or_create(name='Sick Leave', defaults={'days_allowed': 15, 'is_paid': True})
        unpaid, _ = LeaveType.objects.get_or_create(name='Unpaid Leave', defaults={'days_allowed': 30, 'is_paid': False})

        leave_data = [
            (employees[2], annual, d(10), d(17), 'approved'),
            (employees[5], sick, d(-2), d(0), 'approved'),
            (employees[8], annual, d(20), d(27), 'pending'),
            (employees[10], annual, d(5), d(9), 'pending'),
        ]
        for lv_d in leave_data:
            LeaveRequest.objects.get_or_create(employee=lv_d[0], start_date=lv_d[2], defaults=dict(
                leave_type=lv_d[1], end_date=lv_d[3], days=(lv_d[3] - lv_d[2]).days, status=lv_d[4]
            ))

        # ── Payroll ────────────────────────────────────────────
        for emp in employees[:6]:
            Payroll.objects.get_or_create(
                employee=emp, period_start=date(2026, 3, 1),
                defaults=dict(
                    period_end=date(2026, 3, 31),
                    base_salary=emp.base_salary,
                    overtime_pay=emp.base_salary * 0.05,
                    allowances=500,
                    bonuses=0,
                    gross_salary=emp.base_salary * 1.05 + 500,
                    tax_deduction=emp.base_salary * 0.05,
                    other_deductions=0,
                    net_salary=emp.base_salary * 1.0 + 500,
                    status='paid',
                    created_by=admin
                )
            )

        # ── Equipment ──────────────────────────────────────────
        cat_crane, _ = EquipmentCategory.objects.get_or_create(name='Cranes')
        cat_vehicle, _ = EquipmentCategory.objects.get_or_create(name='Heavy Vehicles')
        cat_concrete, _ = EquipmentCategory.objects.get_or_create(name='Concrete Equipment')
        cat_earthwork, _ = EquipmentCategory.objects.get_or_create(name='Earthworks')

        equipment_data = [
            ('EQ-001', 'Tower Crane TC-800', cat_crane, 'in_use', 5500, 'PRJ-001 Site', d(-30), d(60)),
            ('EQ-002', 'Mobile Crane MC-350', cat_crane, 'available', 3200, 'Yard', d(-60), d(30)),
            ('EQ-003', 'Concrete Pump CP-60', cat_concrete, 'in_use', 1200, 'PRJ-002 Site', d(-15), d(45)),
            ('EQ-004', 'Concrete Mixer CM-20', cat_concrete, 'available', 800, 'Yard', d(-90), d(10)),
            ('EQ-005', 'Excavator EX-350', cat_earthwork, 'maintenance', 2800, 'Workshop', d(-45), d(5)),
            ('EQ-006', 'Bulldozer BD-200', cat_earthwork, 'in_use', 2200, 'PRJ-005 Site', d(-20), d(40)),
            ('EQ-007', 'Dump Truck DT-25T', cat_vehicle, 'available', 600, 'Yard', d(-10), d(20)),
            ('EQ-008', 'Forklift FL-5T', cat_vehicle, 'in_use', 400, 'PRJ-001 Site', d(-5), d(25)),
            ('EQ-009', 'Piling Rig PR-100', cat_earthwork, 'retired', 4500, 'Yard', d(-200), None),
            ('EQ-010', 'Aerial Work Platform AWP-20', cat_vehicle, 'available', 350, 'Yard', d(-7), d(14)),
        ]
        for eq_d in equipment_data:
            Equipment.objects.get_or_create(code=eq_d[0], defaults=dict(
                name=eq_d[1], category=eq_d[2], status=eq_d[3],
                cost_per_day=eq_d[4], location=eq_d[5],
                last_maintenance=eq_d[6], next_maintenance=eq_d[7],
                purchase_cost=eq_d[4] * 500, current_value=eq_d[4] * 300
            ))

        # Maintenance records
        eq1 = Equipment.objects.get(code='EQ-005')
        MaintenanceRecord.objects.get_or_create(equipment=eq1, scheduled_date=d(-45), defaults=dict(
            maintenance_type='Major Service', status='completed', completed_date=d(-43), cost=4500, performed_by='Al Futtaim Service Center'
        ))
        MaintenanceRecord.objects.get_or_create(equipment=eq1, scheduled_date=d(5), defaults=dict(
            maintenance_type='Engine Overhaul', status='in_progress', cost=8000
        ))

        # ── Materials ──────────────────────────────────────────
        cat_cem, _ = MaterialCategory.objects.get_or_create(name='Cement & Concrete')
        cat_steel, _ = MaterialCategory.objects.get_or_create(name='Steel & Rebar')
        cat_timber, _ = MaterialCategory.objects.get_or_create(name='Timber & Formwork')
        cat_pipes, _ = MaterialCategory.objects.get_or_create(name='Pipes & Fittings')
        cat_elec, _ = MaterialCategory.objects.get_or_create(name='Electrical Materials')

        materials_data = [
            ('MAT-001', 'Portland Cement OPC 53', cat_cem, 'bag', 25, 8500, 2000),
            ('MAT-002', 'Ready Mix Concrete C40', cat_cem, 'm3', 285, 95, 200),
            ('MAT-003', 'Ready Mix Concrete C25', cat_cem, 'm3', 240, 200, 150),
            ('MAT-004', 'Steel Rebar 12mm', cat_steel, 'ton', 780, 45, 80),
            ('MAT-005', 'Steel Rebar 16mm', cat_steel, 'ton', 810, 60, 80),
            ('MAT-006', 'Steel Rebar 20mm', cat_steel, 'ton', 830, 25, 50),
            ('MAT-007', 'Structural Steel H-Beam', cat_steel, 'ton', 1150, 18, 30),
            ('MAT-008', 'Plywood Formwork 18mm', cat_timber, 'unit', 45, 320, 100),
            ('MAT-009', 'Timber Scaffolding Plank', cat_timber, 'm', 8, 450, 200),
            ('MAT-010', 'uPVC Pipe 200mm', cat_pipes, 'm', 32, 600, 300),
            ('MAT-011', 'GI Pipe 100mm', cat_pipes, 'm', 48, 180, 200),
            ('MAT-012', 'XLPE Cable 3x16mm', cat_elec, 'm', 18, 500, 400),
            ('MAT-013', 'Distribution Board 24-way', cat_elec, 'unit', 420, 8, 5),
        ]
        for mat_d in materials_data:
            Material.objects.get_or_create(code=mat_d[0], defaults=dict(
                name=mat_d[1], category=mat_d[2], unit=mat_d[3],
                unit_cost=mat_d[4], current_stock=mat_d[5], reorder_level=mat_d[6], minimum_stock=mat_d[6] * 0.5
            ))

        # ── Vendors ────────────────────────────────────────────
        vendors_data = [
            ('VND-001', 'Gulf Steel Trading LLC', 'supplier', 'Hassan Al Ali', 'hassan@gulfsteel.ae', '+971-4-555-1001', 4.5),
            ('VND-002', 'Arabian Cement Company', 'supplier', 'Mohammed Nasser', 'mnasser@aracem.ae', '+971-2-555-1002', 4.8),
            ('VND-003', 'Emirates Ready Mix', 'supplier', 'James Brown', 'jbrown@emirm.ae', '+971-4-555-1003', 4.2),
            ('VND-004', 'Al Futtaim Heavy Equipment', 'equipment', 'Ravi Kumar', 'ravi@alfuttaim.ae', '+971-4-555-1004', 4.7),
            ('VND-005', 'BuildTech Formwork Solutions', 'supplier', 'David Lee', 'dlee@buildtech.ae', '+971-6-555-1005', 3.9),
            ('VND-006', 'Delta Electrical Supplies', 'supplier', 'Amira Khalil', 'amira@delta.ae', '+971-4-555-1006', 4.1),
            ('VND-007', 'Al Nabooda Crane Services', 'subcontractor', 'Tariq Al Nabooda', 'tariq@alnabooda.ae', '+971-4-555-1007', 4.6),
            ('VND-008', 'Transguard Logistics', 'service', 'Paul Smith', 'psmith@transguard.ae', '+971-4-555-1008', 4.0),
        ]
        vendors = []
        for v_d in vendors_data:
            v, _ = Vendor.objects.get_or_create(code=v_d[0], defaults=dict(
                name=v_d[1], category=v_d[2], contact_person=v_d[3],
                email=v_d[4], phone=v_d[5], rating=v_d[6], status='active'
            ))
            vendors.append(v)

        # ── Purchase Orders ────────────────────────────────────
        mat_steel = Material.objects.get(code='MAT-005')
        mat_cement = Material.objects.get(code='MAT-001')
        mat_concrete = Material.objects.get(code='MAT-002')
        mat_cable = Material.objects.get(code='MAT-012')

        po_data = [
            ('PO-2026-001', p1, vendors[0], d(-45), d(-30), 'received', mat_steel, 50, 810),
            ('PO-2026-002', p1, vendors[1], d(-30), d(-15), 'received', mat_cement, 2000, 25),
            ('PO-2026-003', p2, vendors[2], d(-20), d(-5), 'partial', mat_concrete, 200, 285),
            ('PO-2026-004', p5, vendors[0], d(-10), d(10), 'approved', mat_steel, 80, 810),
            ('PO-2026-005', p1, vendors[5], d(-5), d(15), 'sent', mat_cable, 300, 18),
            ('PO-2026-006', p3, vendors[1], d(5), d(25), 'pending', mat_cement, 500, 25),
        ]
        for po_d in po_data:
            subtotal = po_d[7] * po_d[8]
            tax = subtotal * 0.05
            po, _ = PurchaseOrder.objects.get_or_create(po_number=po_d[0], defaults=dict(
                project=po_d[1], vendor=po_d[2], date=po_d[3], expected_delivery=po_d[4],
                status=po_d[5], subtotal=subtotal, tax_amount=tax, total_amount=subtotal + tax,
                created_by=admin
            ))
            PurchaseOrderItem.objects.get_or_create(purchase_order=po, material=po_d[6], defaults=dict(
                quantity=po_d[7], unit_price=po_d[8], total_price=subtotal,
                received_quantity=po_d[7] if po_d[5] == 'received' else po_d[7] * 0.5 if po_d[5] == 'partial' else 0
            ))

        # ── Finance: Budgets ───────────────────────────────────
        cat_labor, _ = BudgetCategory.objects.get_or_create(code='LAB', defaults={'name': 'Labor & Manpower'})
        cat_mat, _ = BudgetCategory.objects.get_or_create(code='MAT', defaults={'name': 'Materials'})
        cat_eq, _ = BudgetCategory.objects.get_or_create(code='EQP', defaults={'name': 'Equipment'})
        cat_sub, _ = BudgetCategory.objects.get_or_create(code='SUB', defaults={'name': 'Subcontractors'})
        cat_oh, _ = BudgetCategory.objects.get_or_create(code='OH', defaults={'name': 'Overhead & Preliminaries'})

        for proj, split in [(p1, [0.30, 0.40, 0.15, 0.10, 0.05]), (p2, [0.25, 0.45, 0.15, 0.10, 0.05])]:
            budget, _ = Budget.objects.get_or_create(project=proj, defaults=dict(
                total_amount=proj.budget, contingency_percentage=10, approved_by=admin
            ))
            for cat, pct, actual_pct in zip([cat_labor, cat_mat, cat_eq, cat_sub, cat_oh], split, [0.4, 0.35, 0.3, 0.2, 0.5]):
                estimated = proj.budget * pct
                BudgetItem.objects.get_or_create(budget=budget, category=cat, defaults=dict(
                    description=cat.name, estimated_amount=estimated,
                    actual_amount=estimated * actual_pct * (proj.completion_percentage / 100 + 0.1)
                ))

        # ── Invoices ───────────────────────────────────────────
        invoices_data = [
            ('INV-2025-001', p4, d(-200), d(-170), 5600000, 'paid'),
            ('INV-2025-002', p4, d(-120), d(-90), 8400000, 'paid'),
            ('INV-2026-001', p1, d(-60), d(-30), 4500000, 'paid'),
            ('INV-2026-002', p1, d(-30), d(0), 3500000, 'partial'),
            ('INV-2026-003', p2, d(-45), d(-15), 2500000, 'paid'),
            ('INV-2026-004', p2, d(-10), d(20), 1800000, 'sent'),
            ('INV-2026-005', p5, d(-5), d(25), 6700000, 'draft'),
            ('INV-2026-006', p3, d(10), d(40), 640000, 'draft'),
        ]
        for inv_d in invoices_data:
            tax = inv_d[4] * 0.05
            total = inv_d[4] + tax
            paid = total if inv_d[5] == 'paid' else total * 0.4 if inv_d[5] == 'partial' else 0
            inv, created = Invoice.objects.get_or_create(invoice_number=inv_d[0], defaults=dict(
                project=inv_d[1], invoice_type='client', date=inv_d[2], due_date=inv_d[3],
                amount=inv_d[4], tax_amount=tax, total_amount=total, paid_amount=paid,
                status=inv_d[5], created_by=admin
            ))
            if created and inv_d[5] in ('paid', 'partial'):
                Payment.objects.create(
                    invoice=inv, date=inv_d[3], amount=paid,
                    method='bank_transfer', reference=f'TRF-{inv_d[0]}', recorded_by=admin
                )

        # ── Expenses ───────────────────────────────────────────
        expenses_data = [
            (p1, 'labor', 'Site Labour – Week 14', 285000, d(-7), 'approved'),
            (p1, 'materials', 'Rebar delivery charges', 4500, d(-10), 'paid'),
            (p1, 'equipment', 'Tower crane monthly rental', 165000, d(-30), 'paid'),
            (p2, 'labor', 'Bridge deck crew – March', 195000, d(-14), 'approved'),
            (p2, 'subcontractor', 'Structural steel erection', 380000, d(-20), 'approved'),
            (p5, 'overhead', 'Site office setup', 45000, d(-5), 'pending'),
            (p5, 'transportation', 'Equipment mobilization', 28000, d(-3), 'pending'),
            (p1, 'utilities', 'Temporary power supply', 12000, d(-15), 'paid'),
        ]
        for exp_d in expenses_data:
            Expense.objects.get_or_create(
                project=exp_d[0], description=exp_d[2], date=exp_d[3],
                defaults=dict(category=exp_d[1], amount=exp_d[4], status=exp_d[5], submitted_by=admin)
            )

        # ── Document Categories & Documents ────────────────────
        doc_cats = {}
        for cat_name in ['Drawings', 'Specifications', 'Contracts', 'Reports', 'Permits', 'Inspection Records']:
            dc, _ = DocumentCategory.objects.get_or_create(name=cat_name)
            doc_cats[cat_name] = dc

        docs_data = [
            (p1, 'Architectural Drawings – Tower A', 'DWG-001', doc_cats['Drawings'], 'approved', '3.0'),
            (p1, 'Structural Design Calculations', 'SPEC-001', doc_cats['Specifications'], 'approved', '2.1'),
            (p1, 'Main Construction Contract', 'CON-001', doc_cats['Contracts'], 'approved', '1.0'),
            (p1, 'Monthly Progress Report – March', 'RPT-001', doc_cats['Reports'], 'approved', '1.0'),
            (p1, 'Building Permit', 'PRM-001', doc_cats['Permits'], 'approved', '1.0'),
            (p2, 'Bridge Design Drawings', 'DWG-002', doc_cats['Drawings'], 'review', '2.0'),
            (p2, 'Foundation Inspection Report', 'INS-001', doc_cats['Inspection Records'], 'approved', '1.0'),
            (p2, 'Traffic Management Plan', 'SPEC-002', doc_cats['Specifications'], 'approved', '1.1'),
            (p5, 'Master Infrastructure Plan', 'DWG-003', doc_cats['Drawings'], 'draft', '0.5'),
            (p3, 'Road Design Drawings', 'DWG-004', doc_cats['Drawings'], 'draft', '0.1'),
        ]
        for doc_d in docs_data:
            Document.objects.get_or_create(project=doc_d[0], document_number=doc_d[2], defaults=dict(
                name=doc_d[1], category=doc_d[3], status=doc_d[4], version=doc_d[5], uploaded_by=admin
            ))

        # ── Resource Allocations ───────────────────────────────
        eq_crane = Equipment.objects.get(code='EQ-001')
        eq_pump = Equipment.objects.get(code='EQ-003')
        for proj, eq in [(p1, eq_crane), (p2, eq_pump)]:
            ResourceAllocation.objects.get_or_create(project=proj, equipment=eq, defaults=dict(
                resource_type='equipment', quantity=1, start_date=d(-30), end_date=d(90)
            ))

        self.stdout.write(self.style.SUCCESS(f"""
✅ Test data loaded successfully!

Summary:
  Projects   : {Project.objects.count()}
  Employees  : {Employee.objects.count()}
  Equipment  : {Equipment.objects.count()}
  Materials  : {Material.objects.count()}
  Vendors    : {Vendor.objects.count()}
  PO's       : {PurchaseOrder.objects.count()}
  Invoices   : {Invoice.objects.count()}
  Documents  : {Document.objects.count()}

Login: admin / admin123
        """))
