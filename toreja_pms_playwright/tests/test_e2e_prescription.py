# =============================================================================
# tests/test_e2e_prescription.py  — Playwright version
# =============================================================================

import pytest
from playwright.sync_api import Page

from pages.dashboard_page import DashboardPage
from pages.patients_page import PatientsPage
from pages.medicines_page import MedicinesPage
from pages.new_prescription_page import NewPrescriptionPage
from pages.patient_history_page import PatientHistoryPage
from test_data.test_data import E2EData
from utils.logger import get_logger
from utils.test_step import step
from utils.config import Config

logger = get_logger(__name__)


@pytest.mark.e2e
@pytest.mark.usefixtures("e2e_page")
class TestPrescriptionWorkflow:

    patient_name:  str = ""
    medicine_name: str = ""

    @pytest.mark.run(order=1)
    def test_01_dashboard_loads(self, e2e_page: Page):
        logger.info("=== E2E STAGE 1: Verify dashboard ===")
        dashboard = DashboardPage(e2e_page)

        with step("URL contains dashboard.php"):
            assert "dashboard.php" in e2e_page.url

        with step("Welcome message visible"):
            welcome = dashboard.get_welcome_text()
            assert "Welcome" in welcome

        with step("All four stat boxes visible"):
            assert dashboard.is_today_box_displayed()
            assert dashboard.is_week_box_displayed()
            assert dashboard.is_month_box_displayed()
            assert dashboard.is_year_box_displayed()

        logger.info("STAGE 1 PASSED")

    @pytest.mark.run(order=2)
    def test_02_add_new_patient(self, e2e_page: Page):
        logger.info("=== E2E STAGE 2: Add patient ===")
        patient_data = E2EData.patient()
        TestPrescriptionWorkflow.patient_name = patient_data["name"]
        logger.info(f"Patient: {self.patient_name}")

        page = PatientsPage(e2e_page)

        with step("Navigate to patients page"):
            page.open()
            assert page.is_on_page()

        with step("Add patient form"):
            page.add_patient(**patient_data)

        with step("Verify patient in table"):
            e2e_page.wait_for_load_state("domcontentloaded")
            assert page.is_patient_in_table(patient_data["name"])

        logger.info("STAGE 2 PASSED")

    @pytest.mark.run(order=3)
    def test_03_add_new_medicine(self, e2e_page: Page):
        logger.info("=== E2E STAGE 3: Add medicine ===")
        TestPrescriptionWorkflow.medicine_name = E2EData.medicine()
        logger.info(f"Medicine: {self.medicine_name}")

        page = MedicinesPage(e2e_page)

        with step("Navigate to medicines page"):
            page.open()
            assert page.is_on_page()

        with step("Add medicine"):
            page.add_medicine(self.medicine_name)

        with step("Verify medicine in table"):
            e2e_page.wait_for_load_state("domcontentloaded")
            assert page.is_medicine_in_table(self.medicine_name)

        logger.info("STAGE 3 PASSED")

    @pytest.mark.run(order=4)
    def test_04_create_prescription(self, e2e_page: Page):
        logger.info("=== E2E STAGE 4: Create prescription ===")

        if not self.patient_name or not self.medicine_name:
            pytest.skip("Skipping — patient or medicine setup failed in earlier stage")

        page = NewPrescriptionPage(e2e_page)

        with step("Navigate to new prescription"):
            page.open()
            assert page.is_on_page()

        with step("Select patient"):
            page.select_patient(self.patient_name)

        with step("Fill visit date"):
            page.set_visit_date(E2EData.VISIT_DATE)

        with step("Fill next visit date"):
            page.set_next_visit_date(E2EData.NEXT_VISIT_DATE)

        with step("Fill BP"):
            page.enter_bp(E2EData.BP)

        with step("Fill weight"):
            page.enter_weight(E2EData.WEIGHT)

        with step("Fill disease"):
            page.enter_disease(E2EData.DISEASE)

        with step("Add medicine row"):
            page.click_add_row()
            assert page.get_row_count() >= 1

        with step("Fill medicine row"):
            page.fill_medicine_row(
                row_index=1,
                medicine=self.medicine_name,
                frequency=E2EData.FREQUENCY,
                timing=E2EData.TIMING,
                qty=E2EData.QTY,
                dosage=E2EData.DOSAGE,
            )

        with step("Save prescription"):
            page.click_save_prescription()
            e2e_page.wait_for_timeout(1500)

        logger.info("STAGE 4 PASSED")

    @pytest.mark.run(order=5)
    def test_05_verify_patient_history(self, e2e_page: Page):
        logger.info("=== E2E STAGE 5: Verify history ===")

        if not self.patient_name:
            pytest.skip("patient_name not set — did test_02 pass?")

        page = PatientHistoryPage(e2e_page)

        with step("Navigate to patient history"):
            page.open()
            assert page.is_on_page()

        with step("Search patient history"):
            page.search_patient_history(self.patient_name)

        with step("Assert history rows exist"):
            try:
                e2e_page.wait_for_function(
                    "() => document.querySelectorAll('#patient_history tbody tr').length > 0",
                    timeout=Config.TIMEOUT
                )
            except Exception:
                pytest.fail(
                    f"No history rows for '{self.patient_name}' — check if prescription saved"
                )
            assert page.get_result_row_count() > 0

        with step("Assert disease in history"):
            disease_cell = page.get_cell_text(row=1, col=3)
            assert E2EData.DISEASE.lower() in disease_cell.lower(), \
                f"Expected '{E2EData.DISEASE}', got '{disease_cell}'"

        with step("Assert medicine in history"):
            medicine_cell = page.get_cell_text(row=1, col=4)
            assert self.medicine_name.lower() in medicine_cell.lower(), \
                f"Expected '{self.medicine_name}', got '{medicine_cell}'"

        logger.info("STAGE 5 PASSED — full E2E workflow complete")
