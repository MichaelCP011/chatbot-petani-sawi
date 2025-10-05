# =============================================================================
# Bagian 1: Import Library & Konfigurasi
# =============================================================================
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

print(f"TensorFlow Version: {tf.__version__}")

# --- Konfigurasi Utama ---
# Anda bisa mengubah parameter ini untuk eksperimen
IMAGE_SIZE = (224, 224)
BATCH_SIZE = 32
INITIAL_EPOCHS = 15      # Jumlah epoch untuk training awal
FINE_TUNE_EPOCHS = 10      # Jumlah epoch untuk fine-tuning
DATASET_PATH = '.'
LEARNING_RATE_INITIAL = 0.001
LEARNING_RATE_FINE_TUNE = 0.00001


# =============================================================================
# Bagian 2: Memuat dan Menyiapkan Dataset
# =============================================================================
print("Memuat dataset dari direktori...")

train_dataset = tf.keras.utils.image_dataset_from_directory(
    f"{DATASET_PATH}/train",
    shuffle=True,
    image_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE,
    label_mode='categorical'
)

validation_dataset = tf.keras.utils.image_dataset_from_directory(
    f"{DATASET_PATH}/val",
    shuffle=False,
    image_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE,
    label_mode='categorical'
)

test_dataset = tf.keras.utils.image_dataset_from_directory(
    f"{DATASET_PATH}/test",
    shuffle=False,
    image_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE,
    label_mode='categorical'
)

class_names = train_dataset.class_names
num_classes = len(class_names)
print(f"Berhasil memuat dataset. Ditemukan {num_classes} kelas: {class_names}")

# Optimasi performa dataset
AUTOTUNE = tf.data.AUTOTUNE
train_dataset = train_dataset.prefetch(buffer_size=AUTOTUNE)
validation_dataset = validation_dataset.prefetch(buffer_size=AUTOTUNE)
test_dataset = test_dataset.prefetch(buffer_size=AUTOTUNE)


# =============================================================================
# Bagian 3: Membangun Arsitektur Model
# =============================================================================
print("Membangun arsitektur model...")

data_augmentation = keras.Sequential([
    layers.RandomFlip("horizontal_and_vertical"),
    layers.RandomRotation(0.2),
    layers.RandomZoom(0.1),
])

# Gunakan 'layers.Rescaling' sebagai pengganti fungsi preprocess_input
# untuk memastikan model dapat disimpan dan dimuat tanpa masalah.
# Skala [0, 255] menjadi [-1, 1]
preprocess_layer = layers.Rescaling(1./127.5, offset=-1)

base_model = tf.keras.applications.MobileNetV2(
    input_shape=(224, 224, 3),
    include_top=False,
    weights='imagenet'
)
base_model.trainable = False

inputs = keras.Input(shape=(224, 224, 3))
x = data_augmentation(inputs)
x = preprocess_layer(x)
x = base_model(x, training=False)
x = layers.GlobalAveragePooling2D()(x)
x = layers.Dropout(0.2)(x)
outputs = layers.Dense(num_classes, activation='softmax')(x)
model = keras.Model(inputs, outputs)


# =============================================================================
# Bagian 4: Training Awal (Feature Extraction)
# =============================================================================
print("\nMemulai Tahap 1: Training Awal (Feature Extraction)...")
model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=LEARNING_RATE_INITIAL),
    loss="categorical_crossentropy",
    metrics=["accuracy"]
)

history = model.fit(
    train_dataset,
    epochs=INITIAL_EPOCHS,
    validation_data=validation_dataset
)


# =============================================================================
# Bagian 5: Fine-Tuning
# =============================================================================
print("\nMemulai Tahap 2: Fine-Tuning...")

# Buka gembok base_model
base_model.trainable = True

# Bekukan semua lapisan kecuali 30 lapisan terakhir
fine_tune_at = len(base_model.layers) - 30
for layer in base_model.layers[:fine_tune_at]:
    layer.trainable = False

# Compile ulang model dengan learning rate yang sangat kecil
model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=LEARNING_RATE_FINE_TUNE),
    loss="categorical_crossentropy",
    metrics=["accuracy"]
)

# Lanjutkan training
total_epochs = INITIAL_EPOCHS + FINE_TUNE_EPOCHS
history_fine = model.fit(
    train_dataset,
    epochs=total_epochs,
    initial_epoch=history.epoch[-1],
    validation_data=validation_dataset
)


# =============================================================================
# Bagian 6: Evaluasi Final dan Penyimpanan Model
# =============================================================================
print("\nMelakukan evaluasi akhir dengan test dataset...")

loss, accuracy = model.evaluate(test_dataset)
print("-" * 30)
print(f"Final Test Accuracy: {accuracy * 100:.2f}%")
print(f"Final Test Loss: {loss:.4f}")
print("-" * 30)

# Simpan model final dalam format .keras yang modern
model_filename = "chili_disease_model_final.keras"
model.save(model_filename)
print(f"Model final telah disimpan dalam file: '{model_filename}'")