GREETING_TEMPLATE = """Hello,

I have received your request and will begin working on this ticket. Please monitor this ticket closely in case any additional information is needed.

Thank you,
Tu Nguyen"""


MANDARIN_GREETING_TEMPLATE = """我们很高兴为您提供中英双语服务。接下来您可以任意选择中文或英文来更新此工单。

尊敬的供应商团队， 

您好！

我们已收到您的请求，并将开始处理此工单。 

请您密切关注此工单，以便在需要时提供补充信息。 

祝好，

Tu Nguyen


We’re happy to support you in both Mandarin and English. Please feel free to continue the conversation in your preferred language.

Hello,

I have received your request and will begin working on this ticket. Please monitor this ticket closely in case any additional information is needed.

Thank you,
Tu Nguyen"""


NORMAL_DONE_TEMPLATE = """Hello,

We have finished this ticket today. Details can be found in this attachment.
Please allow 24-48 hours for changes to reflect on-site. If changes are not displayed after this time, please add a comment to reopen the ticket and we will work on resolving the issue. If you have a new request to have updates made, we would ask that a new ticket be entered!

Thank you,
Tu Nguyen"""


MANDARIN_NORMAL_DONE_TEMPLATE = """尊敬的供应商团队，

您好！

此工单已于今日完成。详细信息请参阅附件。

请等待 24-48 小时，以便更改在网站上生效。如果在 48 小时后更改仍未显示，请添加评论以重新开启工单，我们将继续协助您解决此问题。

如您有新的更新需求，请提交一张新的工单。

祝好，

Tu Nguyen


Hello,

We have finished this ticket today. Details can be found in this attachment.
Please allow 24-48 hours for changes to reflect on-site. If changes are not displayed after this time, please add a comment to reopen the ticket and we will work on resolving the issue. If you have a new request to have updates made, we would ask that a new ticket be entered!

Thank you,
Tu Nguyen"""


EXCLUDED_DONE_TEMPLATE = """Hello,

We have finished this ticket today, but {number} SKUs have been excluded from the request due to {reason}. Details can be found in this attachment.
Please allow 24-48 hours for changes to reflect on-site. If changes are not displayed after this time, please add a comment to reopen the ticket and we will work on resolving the issue. If you have a new request to have updates made, we would ask that a new ticket be entered!

Thank you,
Tu Nguyen"""


MANDARIN_EXCLUDED_DONE_TEMPLATE = """尊敬的供应商团队，

您好！

此工单已于今日完成，但由于 {reason}，已有 {number} 个 SKU 从请求中排除。详细信息请参阅附件。

请等待 24-48 小时，以便更改在网站上生效。如果在 48 小时后更改仍未显示，请添加评论以重新开启工单，我们将继续协助您解决此问题。

如您有新的更新需求，请提交一张新的工单。

祝好，

Tu Nguyen


Hello,

We have finished this ticket today, but {number} SKUs have been excluded from the request due to {reason}. Details can be found in this attachment.
Please allow 24-48 hours for changes to reflect on-site. If changes are not displayed after this time, please add a comment to reopen the ticket and we will work on resolving the issue. If you have a new request to have updates made, we would ask that a new ticket be entered!

Thank you,
Tu Nguyen"""


# ============================================================
# CANCEL TEMPLATES
# ============================================================

CANCEL_REROUTE_TEMPLATE = """[Public Comment]
Hello,

We've completed request [{request_id}]. I am rerouting this ticket to the {team_name} to {update_details}. They will provide you with an update shortly!

Thank you,
Tu Nguyen

----------------------------------------
[Internal Note]
Team: {target_team}
Initial Update: {initial_update}
Summary: {summary}
Action Requested: {action_requested}
Next Steps: {next_steps}"""


CANCEL_ONSITE_TEMPLATE = """Hello,

Thank you for reaching out regarding the storefront issue. We have flagged your concern to our tech team for further investigation. We will be closing this ticket while the tech team assists.

Please let us know if you have any questions.

Best Regards,
Tu Nguyen"""


CANCEL_DUPLICATE_TEMPLATE = """Hi Supplier Team,

Thank you for your request. Upon further checking, we have confirmed that this ticket request is a duplicate of the ticket request {original_ticket}. Please expect an update on {original_ticket} itself soon.

We will be closing this duplicate ticket. If you have any questions or feel like the request is different from the duplicate ticket, please don't hesitate to reopen this ticket. Thank you for your understanding.

Thank you,
Tu Nguyen"""


CANCEL_ALREADY_IN_TARGET_TEMPLATE = """Hello,

Upon our checking, SKU {sku} is currently under the {target_type} ({target_name}).

Since no further action from our end is needed, we will be closing this ticket.

Thank you,
Tu Nguyen"""


CANCEL_SF_DISPLAY_BUG_TEMPLATE = """Hello, thank you for your ticket

We are currently experiencing issues with our replatformed SF display and have submitted a ticket flagging your concern. We will be closing this ticket while the tech team assists.

Please let us know if you have any questions,
Tu Nguyen"""


CANCEL_WAITING_AUTHOR_3DAYS_TEMPLATE = """Hello,

This ticket has surpassed its time on pause, so we will be closing this ticket. We ask that once you have the clarification we need to proceed with completing this ticket, you leave a comment on this ticket to re-open it.

Thanks,
Tu Nguyen"""


CANCEL_MASTER_NOT_CORE_CLASS_TEMPLATE = """Hello,

The reason this SKU [or these SKUs] could not be moved into Exclusive Brands is because their Master Class is not a Core Class (meaning it is a class Wayfair does not have in our Exclsuive Brands). Some factors as to why some classes are ineligible for White Labeling are that the classes are primarily style agnostic, and are differentiated based on function. Additionally, classes that are more likely to be recognized by brand name (such as appliances) are excluded.

Thank you,
Tu Nguyen"""


CANCEL_BAD_STATUS_TEMPLATE = """Hello,

The reason this SKU [or these SKUs] could not be moved into Exclusive Brands is because they are not live on-site. Our tools are only able to process SKUs that are live on Wayfair's site. There are a variety of "bad statuses" that make a SKU inaccesssible on site, and thus, unable to be moved into Exclusive Brands. Examples of bad statuses include "Supplier Discontinued" and "Missing Imagery." [if responding to exclusion] Please reach out to Findability to correct this, then submit a subsequent White Label ticket.

Thank you, 
Tu Nguyen"""


CANCEL_MULTI_SOURCE_SKU_TEMPLATE = """Hello,

We have completed this ticket today, but cannot proceed with the request of {number} SKUs because of the sku set up. Suppliers should reach out to their Supplier Relationship Manager or Category Manager with any questions about the excluded SKUs, and Wayfair employees should reach out to #merch-cat-mgmt-help.

Thank you, 
Tu Nguyen"""


# ============================================================
# ON HOLD TEMPLATES (STANDARD)
# ============================================================

ON_HOLD_GENERAL_TEMPLATE = """Hello,

Thank you for reaching out. We need additional information to complete your request:

Could you please provide the correct part numbers or SKUs you would like us to proceed with, so we can assist you in resolving the issue?

If we have not received a response in 3 day's time we will close this ticket due to lack of response.

Thank you,
Tu Nguyen"""


ON_HOLD_UNLOCATED_SKU_TEMPLATE = """Hello,

Thank you for reaching out. We need additional information to complete your request:

We are unable to locate the part numbers or SKUs: {skus} under supplier "{supplier}" in our database.

Could you please provide the correct SKUs you would like us to proceed with, so we can assist you in resolving the issue?

If we have not received a response in 3 day's time we will close this ticket due to lack of response.

Thank you,
Tu Nguyen"""


ON_HOLD_IH_SRB_FSB_TEMPLATE = """Hello,

Thank you for your patience. We have started working on your request. Since this request involves a Wayfair Specialty Retail or Flagship brand, we are now waiting for approval from our merchant team to proceed.

Thank you,
Tu Nguyen"""


ON_HOLD_IH_APPROVAL_TEMPLATE = """Hello,

Thank you for your patience. We have started working on your request and are now waiting for our In-House team's review to complete this ticket.

Thank you,
Tu Nguyen"""


ON_HOLD_ENGINEERING_BUG_TEMPLATE = """Hello,

Thank you for your patience. We have started working on the request and We've encountered a {issue_summary} issue that needs the support of engineering to resolve. We will be updating you as soon as information is available. In the meanwhile, this ticket's status will be updated to "Paused."

Thank you,
Tu Nguyen"""


ON_HOLD_TOOL_ERROR_TEMPLATE = """Hello,

Thank you for your patience. We are still waiting for engineering to fix tool-related issues. We will be updating you as soon as information is available.

Thank you,
Tu Nguyen"""


ON_HOLD_SPECIFIC_COLLECTION_TEMPLATE = """Hello,

When suppliers agree to participate in our Exclusive Brands program, they do not get to choose the brand or collection name for their SKUs.
If you would still like to update the collection name, Wayfair can assign one for you from a pre-approved list of names.

Please let us know how you would like to proceed.

This ticket will remain open for 3 business days, and if we have not received a response by that time, the ticket will be closed.

Thank you,
Tu Nguyen"""


ON_HOLD_BRAND_CHANGE_TEMPLATE = """Hello,

When suppliers agree to participate in our Exclusive Brands program, they do not get to choose the brand or collection name for their SKUs. If you would still like to move SKUs to a new Exclusive Brand, the Wayfair EB team will decide on the brand for these SKUs based on Wayfair's standards (style and price point), and a new collection name from a pre-approved list of names.

Please let us know how you would like to proceed.

This ticket will remain open for 3 business days, and if we have not received a response by that time, the ticket will be closed.

Thank you,
Tu Nguyen"""


ON_HOLD_TARGET_COLLECTION_INFO_TEMPLATE = """Hello,

We see that you are interested in updating an existing collection, but we need additional information to complete your request. Can you please help us identify the target collection by sharing one or more of the SKUs in the collection you wish to update/move SKUs into?

Thank you,
Tu Nguyen"""


# ============================================================
# ON HOLD TEMPLATES (VAULT / PRIORITY SKU LIST)
# ============================================================

ON_HOLD_VAULT_FULL_WHITE_LABEL_TEMPLATE = """Hi {name}, 
Thank you for reaching out with this white label request.  

We wanted to let you know that {sku_list} {is_are} included in one of our priority SKU lists which now requires elevated internal approval for this merchandising change as it could potentially impact:

- Sort rank & PLAs

- SKU Brand

- Product Description

Before moving forward with execution on your request, this request will be internally reviewed to confirm if we can proceed. Please note, this will slightly extend the turnaround time. You will be notified on this ticket if the request is approved. If you no longer want to move forward with this request, please let us know.

Thank you for your patience and understanding.
Tu Nguyen"""


ON_HOLD_VAULT_PARTIAL_WHITE_LABEL_TEMPLATE = """Hi {name}, 
Thank you for reaching out with this white label request.  

We wanted to let you know that {sku_list} {is_are} included in one of our priority SKU lists which now requires elevated internal approval for this merchandising change as it could impact:

- SKU brand 

Before moving forward with execution on your request, this request will be internally reviewed to confirm if we can proceed. Please note, this will slightly extend the turnaround time. You will be notified on this ticket if the request is approved. If you no longer want to move forward with this request, please let us know.

Thank you for your patience and understanding.
Tu Nguyen"""


ON_HOLD_VAULT_COLLECTION_UPDATE_TEMPLATE = """Hi {name}, 
Thank you for reaching out with this white label request.  

We wanted to let you know that {sku_list} {is_are} included in one of our priority SKU lists which now requires elevated internal approval for this merchandising change as it could impact:

- SKU collection

Before moving forward with execution on your request, this request will be internally reviewed to confirm if we can proceed. Please note, this will slightly extend the turnaround time. You will be notified on this ticket if the request is approved. If you no longer want to move forward with this request, please let us know.

Thank you for your patience and understanding.
Tu Nguyen"""


ON_HOLD_VAULT_UN_WHITE_LABEL_TEMPLATE = """Hi {name}, 
Thank you for reaching out with this un-white label request.  

We wanted to let you know that {sku_list} {is_are} included in one of our priority SKU lists which now requires elevated internal approval for this merchandising change as it could impact:

- SKU brand

Before moving forward with execution on your request, this request will be internally reviewed to confirm if we can proceed. Please note, this will slightly extend the turnaround time. You will be notified on this ticket if the request is approved. If you no longer want to move forward with this request, please let us know.

Thank you for your patience and understanding. 
Tu Nguyen"""