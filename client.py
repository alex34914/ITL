import sys
from typing import Optional, Dict, Any
import requests
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem,
    QPushButton, QDialog, QLineEdit, QFormLayout, QHBoxLayout, QMessageBox
)
from config import API_URL


class ClientApp(QWidget):
    """
    Client application for interacting with the API.

    Provides a GUI to display, add, edit, and delete products.
    """

    def __init__(self) -> None:
        """
        Initializes the main application window.
        """
        super().__init__()
        self.setWindowTitle('Client for API')
        self.setGeometry(100, 100, 800, 600)
        self.init_ui()

    def init_ui(self) -> None:
        """
        Sets up the main UI components.
        """
        layout = QVBoxLayout(self)

        self.table = QTableWidget(self)
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "Name", "Category", "Actions"])
        layout.addWidget(self.table)

        self.add_button = QPushButton("Add New Product", self)
        self.add_button.clicked.connect(self.add_product)
        layout.addWidget(self.add_button)

        self.load_products()
        self.setLayout(layout)

    def load_products(self) -> None:
        """
        Fetches and displays the list of products from the API.
        """
        try:
            response = requests.get(f"{API_URL}/products")
            response.raise_for_status()
            products = response.json()

            self.table.setRowCount(len(products))
            for row_idx, product in enumerate(products):
                self.table.setItem(row_idx, 0, QTableWidgetItem(str(product.get("id"))))
                self.table.setItem(row_idx, 1, QTableWidgetItem(product.get("name")))
                self.table.setItem(row_idx, 2, QTableWidgetItem(product.get("category", "")))

                edit_button = QPushButton("Edit")
                edit_button.clicked.connect(lambda checked, p_id=product.get("id"): self.edit_product(p_id))

                delete_button = QPushButton("Delete")
                delete_button.clicked.connect(lambda checked, p_id=product.get("id"): self.delete_product(p_id))

                actions_layout = QHBoxLayout()
                actions_layout.addWidget(edit_button)
                actions_layout.addWidget(delete_button)

                actions_widget = QWidget()
                actions_widget.setLayout(actions_layout)
                self.table.setCellWidget(row_idx, 3, actions_widget)
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Error", f"Failed to load products:\n{e}")

    def add_product(self) -> None:
        """
        Opens a dialog to add a new product.
        """
        dialog = ProductDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            new_product = dialog.get_product_data()
            try:
                response = requests.post(f"{API_URL}/products", json=new_product)
                if response.status_code == 201:
                    self.load_products()
                else:
                    error = response.json().get("error", "Unknown error")
                    QMessageBox.warning(self, "Error", f"Failed to add product:\n{error}")
            except requests.exceptions.RequestException as e:
                QMessageBox.critical(self, "Error", f"Failed to add product:\n{e}")

    def edit_product(self, product_id: int) -> None:
        """
        Opens a dialog to edit an existing product.

        :param product_id: ID of the product to edit
        """
        try:
            response = requests.get(f"{API_URL}/products/{product_id}")
            response.raise_for_status()
            product_data = response.json()

            dialog = ProductDialog(self, product_data)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                updated_product = dialog.get_product_data()
                response = requests.put(f"{API_URL}/products/{product_id}", json=updated_product)
                if response.status_code == 200:
                    self.load_products()
                else:
                    error = response.json().get("error", "Unknown error")
                    QMessageBox.warning(self, "Error", f"Failed to update product:\n{error}")
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Error", f"Failed to fetch product data:\n{e}")

    def delete_product(self, product_id: int) -> None:
        """
        Deletes a product after user confirmation.

        :param product_id: ID of the product to delete
        """
        reply = QMessageBox.question(
            self, 'Confirm Deletion',
            f"Are you sure you want to delete product ID {product_id}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            try:
                response = requests.delete(f"{API_URL}/products/{product_id}")
                if response.status_code == 200:
                    self.load_products()
                else:
                    error = response.json().get("error", "Unknown error")
                    QMessageBox.warning(self, "Error", f"Failed to delete product:\n{error}")
            except requests.exceptions.RequestException as e:
                QMessageBox.critical(self, "Error", f"Failed to delete product:\n{e}")


class ProductDialog(QDialog):
    """
    Dialog for adding or editing a product.
    """

    def __init__(self, parent: Optional[QWidget] = None, data: Optional[Dict[str, Any]] = None) -> None:
        """
        Initializes the product dialog.

        :param parent: Parent widget
        :param data: Existing product data (optional)
        """
        super().__init__(parent)
        self.setWindowTitle("Product Form")
        self.data = data or {}
        self.init_ui()

    def init_ui(self) -> None:
        """
        Sets up the dialog UI.
        """
        layout = QFormLayout(self)

        self.name_input = QLineEdit(self)
        self.name_input.setText(self.data.get("name", ""))
        layout.addRow("Name:", self.name_input)

        self.category_input = QLineEdit(self)
        self.category_input.setText(self.data.get("category", ""))
        layout.addRow("Category:", self.category_input)

        self.price_input = QLineEdit(self)
        self.price_input.setText(str(self.data.get("price", "")))
        layout.addRow("Price:", self.price_input)

        self.stock_input = QLineEdit(self)
        self.stock_input.setText(str(self.data.get("stock", "")))
        layout.addRow("Stock:", self.stock_input)

        self.description_input = QLineEdit(self)
        self.description_input.setText(self.data.get("description", ""))
        layout.addRow("Description:", self.description_input)

        buttons_layout = QHBoxLayout()
        self.accept_button = QPushButton("OK", self)
        self.accept_button.clicked.connect(self.validate_and_accept)
        self.cancel_button = QPushButton("Cancel", self)
        self.cancel_button.clicked.connect(self.reject)
        buttons_layout.addWidget(self.accept_button)
        buttons_layout.addWidget(self.cancel_button)
        layout.addRow(buttons_layout)

        self.setLayout(layout)

    def validate_and_accept(self) -> None:
        """
        Validates the input fields and accepts the dialog if valid.
        """
        if not self.name_input.text().strip():
            QMessageBox.warning(self, "Validation Error", "Name field cannot be empty.")
            return
        if not self.price_input.text().strip():
            QMessageBox.warning(self, "Validation Error", "Price field cannot be empty.")
            return
        if not self.stock_input.text().strip():
            QMessageBox.warning(self, "Validation Error", "Stock field cannot be empty.")
            return
        try:
            float(self.price_input.text())
        except ValueError:
            QMessageBox.warning(self, "Validation Error", "Price must be a valid number.")
            return
        try:
            int(self.stock_input.text())
        except ValueError:
            QMessageBox.warning(self, "Validation Error", "Stock must be a valid integer.")
            return
        self.accept()

    def get_product_data(self) -> Dict[str, Any]:
        """
        Returns the product data entered in the dialog.

        :return: Product data as a dictionary
        """
        return {
            "name": self.name_input.text(),
            "category": self.category_input.text(),
            "price": float(self.price_input.text()) if self.price_input.text() else 0.0,
            "stock": int(self.stock_input.text()) if self.stock_input.text() else 0,
            "description": self.description_input.text()
        }


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ClientApp()
    window.show()
    sys.exit(app.exec())
