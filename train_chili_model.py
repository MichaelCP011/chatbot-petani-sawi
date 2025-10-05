# =================================================================
# Bagian 1: Import Library & Konfigurasi
# =================================================================
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import matplotlib.pyplot as plt

# Konfigurasi utama
IMAGE_SIZE = (224, 224)  # Ukuran gambar yang akan digunakan model
BATCH_SIZE = 32          # Jumlah gambar yang diproses dalam satu waktu
EPOCHS = 20              # Berapa kali model akan "belajar" dari seluruh dataset
DATASET_PATH = '.'       # Path ke folder dataset ('.' berarti direktori saat ini)

# =================================================================
# Bagian 2: Memuat dan Menyiapkan Dataset
# =================================================================
print("Memuat dataset dari direktori...")

# Memuat data training
train_dataset = tf.keras.utils.image_dataset_from_directory(
    f"{DATASET_PATH}/train",
    shuffle=True,
    image_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE,
    label_mode='categorical' # Label diubah menjadi format one-hot encoding
)

# Memuat data validasi
validation_dataset = tf.keras.utils.image_dataset_from_directory(
    f"{DATASET_PATH}/val",
    shuffle=False,
    image_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE,
    label_mode='categorical'
)

# Memuat data testing
test_dataset = tf.keras.utils.image_dataset_from_directory(
    f"{DATASET_PATH}/test",
    shuffle=False,
    image_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE,
    label_mode='categorical'
)

# Mengambil nama-nama kelas dari nama folder
class_names = train_dataset.class_names
num_classes = len(class_names)
print(f"Berhasil memuat dataset. Ditemukan {num_classes} kelas: {class_names}")

# Optimasi performa dataset agar tidak bottleneck saat training
AUTOTUNE = tf.data.AUTOTUNE
train_dataset = train_dataset.prefetch(buffer_size=AUTOTUNE)
validation_dataset = validation_dataset.prefetch(buffer_size=AUTOTUNE)
test_dataset = test_dataset.prefetch(buffer_size=AUTOTUNE)


# =================================================================
# Bagian 3: Membangun Model dengan Transfer Learning
# =================================================================
print("Membangun arsitektur model...")

# Lapisan untuk augmentasi data (membuat variasi gambar)
data_augmentation = keras.Sequential([
    layers.RandomFlip("horizontal_and_vertical"),
    layers.RandomRotation(0.2),
])

# Mengambil model MobileNetV2 yang sudah dilatih (tanpa lapisan klasifikasi atas)
base_model = tf.keras.applications.MobileNetV2(
    input_shape=(224, 224, 3),
    include_top=False, # Penting! Kita akan buat lapisan atas sendiri
    weights='imagenet'
)

# Membekukan bobot dari base_model agar tidak ikut terlatih ulang
base_model.trainable = False

# Membangun arsitektur akhir
inputs = keras.Input(shape=(224, 224, 3))
x = data_augmentation(inputs)        # Augmentasi data
x = tf.keras.applications.mobilenet_v2.preprocess_input(x) # Preprocessing sesuai MobileNetV2
x = base_model(x, training=False)    # Base model (mode inferensi)
x = layers.GlobalAveragePooling2D()(x) # Meratakan output
x = layers.Dropout(0.2)(x)             # Mencegah overfitting
outputs = layers.Dense(num_classes, activation='softmax')(x) # Lapisan output sesuai jumlah kelas kita

model = keras.Model(inputs, outputs)

# Mencetak ringkasan arsitektur model
model.summary()

# =================================================================
# Bagian 4: Meng-compile dan Melatih Model
# =================================================================
print("Memulai proses training model...")

model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
    loss="categorical_crossentropy",
    metrics=["accuracy"]
)

# Melatih model
history = model.fit(
    train_dataset,
    epochs=EPOCHS,
    validation_data=validation_dataset
)

print("Training selesai.")

# =================================================================
# Bagian 5: Menyimpan Model
# =================================================================
model.save("chili_disease_model.h5")
print("Model telah disimpan dalam file 'chili_disease_model.h5'")