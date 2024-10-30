import json
import os
import matplotlib.pyplot as plt
import numpy as np

def analyze_results(json_file, output_dir='analysis_results'):
    # Load the test results from the JSON file
    with open(json_file, 'r') as f:
        results_list = json.load(f)

    # Initialize counters and data structures
    total_images = len(results_list)
    images_with_detections = 0
    images_without_detections = 0
    total_detections = 0
    detections_per_class = {}
    confidence_scores_per_class = {}
    class_names = set()

    # Process each image's results
    for image_result in results_list:
        detections = image_result['detections']
        if detections:
            images_with_detections += 1
        else:
            images_without_detections += 1

        for det in detections:
            class_name = det['class_name']
            confidence = det['confidence']
            class_names.add(class_name)

            # Update total detections
            total_detections += 1

            # Update detections per class
            detections_per_class[class_name] = detections_per_class.get(class_name, 0) + 1
            confidence_scores_per_class.setdefault(class_name, []).append(confidence)

    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Print summary statistics
    print(f"Total images processed: {total_images}")
    print(f"Images with detections: {images_with_detections}")
    print(f"Images without detections: {images_without_detections}")
    print(f"Total detections: {total_detections}")
    print(f"Detections per class:")
    for class_name in detections_per_class:
        print(f"  {class_name}: {detections_per_class[class_name]}")

    # Save statistics to a text file
    with open(os.path.join(output_dir, 'summary.txt'), 'w') as f:
        f.write(f"Total images processed: {total_images}\n")
        f.write(f"Images with detections: {images_with_detections}\n")
        f.write(f"Images without detections: {images_without_detections}\n")
        f.write(f"Total detections: {total_detections}\n")
        f.write(f"Detections per class:\n")
        for class_name in detections_per_class:
            f.write(f"  {class_name}: {detections_per_class[class_name]}\n")

    # Calculate average confidence per class
    avg_confidence_per_class = {}
    for class_name in confidence_scores_per_class:
        avg_confidence = sum(confidence_scores_per_class[class_name]) / len(confidence_scores_per_class[class_name])
        avg_confidence_per_class[class_name] = avg_confidence
        print(f"Average confidence for {class_name}: {avg_confidence:.2f}")

    # Save average confidence scores
    with open(os.path.join(output_dir, 'average_confidence.txt'), 'w') as f:
        f.write("Average confidence per class:\n")
        for class_name in avg_confidence_per_class:
            f.write(f"  {class_name}: {avg_confidence_per_class[class_name]:.2f}\n")

    # Generate bar chart for detections per class
    plt.figure(figsize=(10, 6))
    classes = list(detections_per_class.keys())
    counts = [detections_per_class[class_name] for class_name in classes]
    plt.bar(classes, counts, color='skyblue')
    plt.xlabel('Class Name')
    plt.ylabel('Number of Detections')
    plt.title('Detections per Class')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'detections_per_class.png'))
    plt.close()

    # Generate bar chart for average confidence per class
    plt.figure(figsize=(10, 6))
    avg_confidences = [avg_confidence_per_class[class_name] for class_name in classes]
    plt.bar(classes, avg_confidences, color='orange')
    plt.xlabel('Class Name')
    plt.ylabel('Average Confidence Score')
    plt.title('Average Confidence per Class')
    plt.xticks(rotation=45)
    plt.ylim(0, 1)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'average_confidence_per_class.png'))
    plt.close()

    # Generate histograms for confidence scores per class
    for class_name in confidence_scores_per_class:
        plt.figure(figsize=(10, 6))
        confidences = confidence_scores_per_class[class_name]
        plt.hist(confidences, bins=10, range=(0, 1), color='green', edgecolor='black')
        plt.xlabel('Confidence Score')
        plt.ylabel('Frequency')
        plt.title(f'Confidence Scores for Class: {class_name}')
        plt.tight_layout()
        filename = f'confidence_histogram_{class_name.replace(" ", "_")}.png'
        plt.savefig(os.path.join(output_dir, filename))
        plt.close()

    # Generate pie chart for class distribution in detections
    plt.figure(figsize=(8, 8))
    plt.pie(counts, labels=classes, autopct='%1.1f%%', startangle=140)
    plt.axis('equal')
    plt.title('Class Distribution in Detections')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'class_distribution_pie_chart.png'))
    plt.close()

    # Optional: List images without detections
    images_no_detections = [img['image_name'] for img in results_list if not img['detections']]
    with open(os.path.join(output_dir, 'images_without_detections.txt'), 'w') as f:
        f.write("Images without detections:\n")
        for image_name in images_no_detections:
            f.write(f"{image_name}\n")

    print(f"\nAnalysis complete. Results saved in the '{output_dir}' directory.")

if __name__ == '__main__':
    # Path to your test results JSON file
    json_file = 'test_results.json'
    analyze_results(json_file)
