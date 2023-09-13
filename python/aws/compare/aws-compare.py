import csv

from ec2-compare import fetch_ec2_details

def write_to_csv(filename, data):
    keys = data[0].keys()
    with open(filename, 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(data)

def main():
    profiles = ['dev', 'hml', 'act', 'prd']
    all_data = []
    differences = []

    # Gather all data
    for profile in profiles:
        all_data.extend(fetch_ec2_details(profile))

    # Write full report
    write_to_csv('full_report.csv', all_data)

    # Generate differences report
    instances_dict = {}
    for item in all_data:
        instance_id = item['Instance ID']
        if instance_id not in instances_dict:
            instances_dict[instance_id] = []
        instances_dict[instance_id].append(item)

    for instance_id, instances in instances_dict.items():
        if len(instances) > 1:  # If instance exists in more than one profile
            base_instance = instances[0]
            for instance in instances[1:]:
                for key, value in instance.items():
                    if key != 'Instance ID' and base_instance[key] != value:
                        differences.append(instance)
                        break

    # Write differences report
    write_to_csv('differences_report.csv', differences)

if __name__ == '__main__':
    main()
