from export_action import report
from export_action.views import AdminExport


def report_to_list(queryset, display_fields, user):
    """ Create list from a report with all data filtering.

    queryset: initial queryset to generate results
    display_fields: list of field references or DisplayField models
    user: requesting user

    Returns list, message in case of issues.
    """
    model_class = queryset.model
    objects = queryset
    message = ""

    if not report._can_change_or_view(model_class, user):
        return [], 'Permission Denied'

    # Convert list of strings to DisplayField objects.
    new_display_fields = []

    for display_field in display_fields:
        field_list = display_field.split('__')
        field = field_list[-1]
        path = '__'.join(field_list[:-1])

        if path:
            path += '__'  # Legacy format to append a __ here.

        df = report.DisplayField(path, field)
        new_display_fields.append(df)

    display_fields = new_display_fields

    # Display Values
    display_field_paths = []
    display_field_names = []

    for i, display_field in enumerate(display_fields):
        model = report.get_model_from_path_string(model_class,
                                                  display_field.path)

        if not model or report._can_change_or_view(model, user):
            display_field_key = display_field.path + display_field.field
            display_field_paths.append(display_field_key)
            if not display_field.path:
                display_field_names.append(
                    str(
                        model._meta.get_field(
                            display_field.field).verbose_name))
            else:
                display_field_names.append(display_field_key)

        else:
            message += 'Error: Permission denied on access to {0}.'.format(
                display_field.name)

    values_list = objects.values_list(*display_field_paths)
    values_and_properties_list = [list(row) for row in values_list]

    return values_and_properties_list, display_field_names, message


def post(self, request, **kwargs):
    context = self.get_context_data(**kwargs)
    fields = []
    for field_name, value in request.POST.items():
        if value == "on":
            fields.append(field_name)
    data_list, fields, message = report_to_list(
        context['queryset'],
        fields,
        self.request.user,
    )
    format = request.POST.get("__format")
    if format == "html":
        return report.list_to_html_response(data_list, header=fields)
    elif format == "csv":
        return report.list_to_csv_response(data_list, header=fields)
    else:
        return report.list_to_xlsx_response(data_list, header=fields)


AdminExport.post = post
