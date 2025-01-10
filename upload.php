<?php
$host = 'localhost';
$dbname = 'pdf_printing_service';
$username = 'root';
$password = '';

// Connect to the database
try {
    $pdo = new PDO("mysql:host=$host;dbname=$dbname", $username, $password);
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
} catch (PDOException $e) {
    die(json_encode(['error' => 'Database connection failed: ' . $e->getMessage()]));
}

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $uploadDir = 'uploads/';
    if (!is_dir($uploadDir)) {
        mkdir($uploadDir, 0777, true);
    }

    $name = $_POST['name'] ?? '';
    $address = $_POST['address'] ?? '';
    $contact = $_POST['contact'] ?? '';
    $gender = $_POST['gender'] ?? 'other';
    $printTime = $_POST['time'] ?? '00:00';
    $bindingOption = $_POST['binding'] ?? 'none';

    if (isset($_FILES['file']) && $_FILES['file']['error'] === UPLOAD_ERR_OK) {
        $fileTmpPath = $_FILES['file']['tmp_name'];
        $fileName = basename($_FILES['file']['name']);
        $fileExtension = strtolower(pathinfo($fileName, PATHINFO_EXTENSION));

        if ($fileExtension !== 'pdf') {
            echo json_encode(['error' => 'Only PDF files are allowed!']);
            exit;
        }

        $newFileName = uniqid('pdf_', true) . '.' . $fileExtension;
        $destination = $uploadDir . $newFileName;

        if (move_uploaded_file($fileTmpPath, $destination)) {
            // Insert file and user details into the database
            try {
                $stmt = $pdo->prepare("INSERT INTO uploads (file_name, binding_option, name, address, contact_number, gender, print_time) VALUES (:file_name, :binding_option, :name, :address, :contact_number, :gender, :print_time)");
                $stmt->execute([
                    ':file_name' => $newFileName,
                    ':binding_option' => $bindingOption,
                    ':name' => $name,
                    ':address' => $address,
                    ':contact_number' => $contact,
                    ':gender' => $gender,
                    ':print_time' => $printTime
                ]);
                echo json_encode([
                    'message' => 'File uploaded and saved successfully!',
                    'fileName' => $fileName,
                    'binding' => $bindingOption,
                    'fileUrl' => 'uploads/' . $newFileName
                ]);
            } catch (PDOException $e) {
                echo json_encode(['error' => 'Database error: ' . $e->getMessage()]);
            }
        } else {
            echo json_encode(['error' => 'File upload failed. Check directory permissions.']);
        }
    } else {
        echo json_encode(['error' => 'No file uploaded or upload error occurred.']);
    }
} else {
    echo json_encode(['error' => 'Invalid request method.']);
}
?>
